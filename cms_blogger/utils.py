import functools
import io
import os

import PIL.Image

from django.template.context import RequestContext
from django.template import Template
from django.utils.encoding import smart_unicode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.base import ContentFile
from django.contrib.sites.models import Site
from django.conf import settings as global_settings
from filer.utils.loader import load_object
from . import settings


def get_from_context(request, what, default=None):
    context = RequestContext(request)
    if hasattr(context, 'bind_template'):
        # Django 1.8: force context processors
        with context.bind_template(Template('')):
            return context.get(what, default)
    return context.get(what, default)


def get_allowed_sites(request, model=None):
    if settings.ALLOWED_SITES_FOR_USER and request and model:
        get_sites_for = load_object(settings.ALLOWED_SITES_FOR_USER)
        return get_sites_for(request.user, model)

    if global_settings.CMS_PERMISSION and request:
        from cms.utils.permissions import get_user_sites_queryset
        return get_user_sites_queryset(request.user)

    return Site.objects.all()


def set_cms_site(f):
    @functools.wraps(f)
    def wrapper(request, *args, **kwds):
        current_site = f(request, *args, **kwds)
        if hasattr(request, 'session'):
            request.session['cms_admin_site'] = current_site.pk
        return current_site
    return wrapper


@set_cms_site
def get_current_site(request, model=None, site_lookup=None):
    site_lookup = (site_lookup or
                   (model and getattr(model, 'site_lookup', None)) or
                   'site__exact')
    if site_lookup in request.REQUEST:
        site_pk = request.REQUEST[site_lookup]
    elif hasattr(request, 'session'):
        site_pk = request.session.get('cms_admin_site', None)

    if site_pk:
        allowed_sites = get_allowed_sites(request, model)
        try:
            return allowed_sites.get(pk=site_pk)
        except Site.DoesNotExist:
            if len(allowed_sites) > 0:
                return allowed_sites[0]

    return Site.objects.get_current()


def user_display_name(user):
    if user.first_name and user.last_name:
        return u'%s %s' % (user.first_name, user.last_name)
    elif user.email:
        return user.email
    else:
        return smart_unicode(user)


def paginate_queryset(queryset, page, max_per_page):
    paginator = Paginator(queryset, max_per_page)
    try:
        paginated_items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_items = paginator.page(paginator.num_pages)
    return paginated_items


class NamedBytesIO(io.BytesIO):
    """
    A simple named bytestream.
    """
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        super(NamedBytesIO, self).__init__(*args, **kwargs)


def image_to_contentfile(image, filename, quality):
    """
    Returns a named bytestream of the input image

    :param image: the image to be stored
    :param filename: the name of the outputfile
    :param quality: the quality of the image
    """
    named_content = NamedBytesIO(name=filename)
    image.save(named_content, quality=quality)
    out_file = ContentFile(content=named_content.getvalue(),
                           name=filename)
    out_file.close()
    return out_file


def calculate_resized_poster_size(size, specs):
    """
    Returns a size tuple with the proper width and height within specs
    bounds. The resulting size keeps aspect ratio from the
    specifications, and will be bounded by the mininum and maximum
    width. If the width is within these bounds it will only resize the
    height to match the aspect ratio.

    :param size: the width, height size tuple
    :param specs: the namespace that contains POSTER_* attributes

    """
    width, height = size
    poster_width = min(max(specs.POSTER_MIN_IMAGE_WIDTH, width),
                       specs.POSTER_IMAGE_WIDTH)
    poster_height = int(round(poster_width / specs.POSTER_IMAGE_ASPECT_RATIO))
    return poster_width, poster_height


def basename_with_extension(filepath, extension='png'):
    """
    Returns the filepath of the input file_object swapped with
    the given extension.

    :param file_object: the input file object
    :param extension: the desired new file extension
    """
    filename, _ = os.path.splitext(os.path.basename(filepath))
    name = ''.join((filename, os.path.extsep, extension))
    return name


def fill_background_image(image, background):
    """
    Returns an image of a certain size that contains the input image
    filled with the given color.

    :param image: the input image
    :param background: the background image

    """
    output_width, output_height = background.size
    input_width, input_height = image.size
    top_left_margin_point = ((output_width - input_width) / 2,
                             (output_height - input_height) / 2)
    background.paste(image, top_left_margin_point)
    return background


def resize_image(image_file, specs=settings, resizer=PIL.Image):
    """
    Resizes an image file based on the width and aspect ratio
    settings;
    Returns a django like image that can be passed to a django
    file/image field.

    :param image_file: the file object that support reading
    :param specs: the namespace object with size specifications attributes
    :param resizer: the resizer implementation object
    """
    image_file.seek(0)
    try:
        image = resizer.open(image_file)
    except IOError as e:
        message_format = 'Cannot open image {image}. Error occured: {error}'
        message = message_format.format(image=image_file.name, error=e)
        raise IOError(message)
    image.load()
    options = {
        'mode': 'RGBA',
        'size': calculate_resized_poster_size(image.size, specs),
        'color': specs.POSTER_IMAGE_FILL_COLOR,
    }
    if options.get('color'):    # we need png to have a trasparent background
        image.thumbnail(options.get('size'), resizer.ANTIALIAS)
        poster_image = fill_background_image(image, resizer.new(**options))
        filename = basename_with_extension(image_file.name, extension='png')
    else:
        poster_image = image
        filename = image_file.name
    django_image_file = image_to_contentfile(poster_image, filename,
                                             specs.POSTER_IMAGE_COMPRESSION)
    return django_image_file
