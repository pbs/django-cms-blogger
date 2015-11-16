from django.http import Http404, HttpResponseNotFound
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from django.db.models import Q
from django.utils import timezone as django_timezone
from cms_layouts.layout_response import LayoutResponse
from .models import BlogEntryPage, Blog, HomeBlog, BlogCategory
from .settings import POSTS_ON_LANDING_PAGE
from .utils import paginate_queryset
import re
import pytz


def get_blog_or_404(slug):
    site = Site.objects.get_current()
    if not slug:
        return get_object_or_404(HomeBlog, site=site)
    return get_object_or_404(Blog, slug=slug, site=site)


def get_entries_queryset(request):
    preview = 'preview' in request.GET and request.user.is_staff
    entry_qs = BlogEntryPage.objects.on_site()
    if not preview:
        entry_qs = entry_qs.published()
    return entry_qs


def entry_page(request, blog_slug, year, month, day, entry_slug):
    """
    View for rendering a blog entry page.

    Timezone changes notes:
    The URL provided to access the blog post represents the date in UTC.
    Making the query with the user timezone will cause missmatches.
    without activate: match tz_transform(UTC DB date, client_tz) with provided UTC url
    with activate: match UTC DB date with provided UTC url

    Date matching is not essential because the slug should be unique.
    """
    entry_qs = get_entries_queryset(request)
    try:
        django_timezone.activate(pytz.utc)
        entry = entry_qs.get(
            publication_date__year=year,
            publication_date__month=month,
            publication_date__day=day,
            slug=entry_slug, blog__slug=blog_slug,
            blog__entries_slugs_with_date=True)
    except BlogEntryPage.DoesNotExist:
        raise Http404
    finally:
        django_timezone.deactivate()

    return entry.render_to_response(request)


def get_terms(query_string):
    query_string = query_string.strip()
    # remove quotes
    query_string = re.sub('\'|\"', '', query_string)
    # strip multiple spaces
    query_string = re.sub('\s{2,}', ' ', query_string)
    return query_string.split()


def get_query(query_string, search_fields):
    terms = get_terms(query_string)
    query = Q()
    for term in terms:
        term_query = Q()
        for field_name in search_fields:
            term_query |= Q(**{"%s__icontains" % field_name: term})
        query &= term_query
    return query


def _paginate_entries_on_blog(request, entries, blog):
    search_q = request.GET.get('q')
    extra_params = ''
    if search_q and search_q.strip():
        extra_params = "&q=%s" % search_q.strip()
        search_fields = ('title', 'short_description')
        entries = entries.filter(get_query(search_q, search_fields))

    entries = paginate_queryset(
        entries, request.GET.get('page'), POSTS_ON_LANDING_PAGE)
    return extra_params, entries


def landing_page(request, blog_slug):
    blog = get_blog_or_404(blog_slug)

    layout = blog.get_layout()
    if not layout:
        return HttpResponseNotFound(
            "<h1>This Landing Page does not have a "
            "layout to render.</h1>")

    extra_params, entries = _paginate_entries_on_blog(
        request, blog.get_entries(), blog)
    context = RequestContext(request)
    context['blog'] = blog
    context['entries'] = entries
    context['extra_params'] = extra_params
    return LayoutResponse(
        blog, layout, request, context=context).make_response()


def category_page(request, blog_slug, slug):
    category = get_object_or_404(
        BlogCategory, blog__slug=blog_slug, slug=slug,
        blog__site=Site.objects.get_current())

    layout = category.get_layout()
    if not layout:
        return HttpResponseNotFound(
            "<h1>This Blog Category Page does not have a "
            "layout to render.</h1>")
    extra_params, entries = _paginate_entries_on_blog(
        request, category.get_entries(), category.blog)
    context = RequestContext(request)
    context['blog'] = category.blog
    context['entries'] = entries
    context['extra_params'] = extra_params
    return LayoutResponse(
        category, layout, request, context=context).make_response()


def entry_or_bio_page(request, blog_slug, slug):
    entry_qs = get_entries_queryset(request)
    try:
        entry = entry_qs.get(
            slug=slug, blog__slug=blog_slug,
            blog__entries_slugs_with_date=False)
    except BlogEntryPage.DoesNotExist:
        raise Http404
    return entry.render_to_response(request)
