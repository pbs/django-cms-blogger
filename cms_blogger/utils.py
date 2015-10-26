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
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        super(NamedBytesIO, self).__init__(*args, **kwargs)



def image_to_file(image, filename):
    named_content = NamedBytesIO(name=filename)
    image.save(named_content)
    out_file = ContentFile(content=named_content.getvalue(),
                           name=filename)
    return out_file


def resize_image(image_file, specs=settings, resizer=PIL.Image):
    """
    Resizes an image file based on the width and aspect ratio settings;
    Returns a django like image that can be passed to a
        django file/image field.
    """
    filename, _ = os.path.splitext(os.path.basename(image_file.name))
    image_file.seek(0)
    try:
        image = resizer.open(image_file)
    except IOError as e:
        message_format = 'Cannot open image {image}. Error occured: {error}'
        message = message_format.format(image=image_file.name, error=e)
        raise IOError(message)
    image.load()
    original_width, original_height = image.size
    poster_width = min(max(specs.POSTER_MIN_IMAGE_WIDTH, original_width),
                       specs.POSTER_IMAGE_WIDTH)
    poster_height = int(round(poster_width / specs.POSTER_IMAGE_ASPECT_RATIO))
    poster_size = poster_width, poster_height
    image.thumbnail(poster_size, resizer.ANTIALIAS)
    thumbnail_width, thumbnail_height = image.size
    poster_image = resizer.new('RGBA', poster_size, 'white')
    center_point = ((poster_width - thumbnail_width) / 2,
                    (poster_height - thumbnail_height) / 2)
    poster_image.paste(image, center_point)
    filepath = ''.join((filename, os.path.extsep, 'png'))
    django_image_file = image_to_file(poster_image, filepath)
    return django_image_file
