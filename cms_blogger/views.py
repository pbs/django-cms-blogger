from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from cms_layouts.layout_response import LayoutResponse
from .models import BlogEntryPage, Blog, BlogCategory
from .settings import POSTS_ON_LANDING_PAGE
import re


def get_entries_queryset_for_request(request):
    preview = 'preview' in request.GET and request.user.is_staff
    entry_qs = BlogEntryPage.objects.on_site()
    if not preview:
        entry_qs = entry_qs.published()
    return entry_qs


def entry_page(request, blog_slug, year, month, day, entry_slug):
    entry_qs = get_entries_queryset_for_request(request)
    try:
        entry = entry_qs.get(
            publication_date__year=year,
            publication_date__month=month,
            publication_date__day=day,
            slug=entry_slug, blog__slug=blog_slug,
            blog__entries_slugs_with_date=True)
    except BlogEntryPage.DoesNotExist:
        raise Http404
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

    paginator = Paginator(entries, POSTS_ON_LANDING_PAGE)
    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        entries = paginator.page(paginator.num_pages)
    return extra_params, entries


def landing_page(request, blog_slug):
    blog = get_object_or_404(
        Blog, slug=blog_slug, site=Site.objects.get_current())
    layout = blog.get_layout()
    if not layout:
        return HttpResponseNotFound(
            "<h1>This Blog Landing Page does not have a "
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
    category = get_object_or_404(BlogCategory,
        blog__slug=blog_slug, slug=slug,
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
    Qblog = blog_slug and Q(blog__slug=blog_slug) or Q(blog__site=Site.objects.get_current())
    entry_qs = get_entries_queryset_for_request(request)

    try:
        entry = entry_qs.get( Q(slug=slug) & Qblog &
            Q(blog__entries_slugs_with_date=False))
    except BlogEntryPage.DoesNotExist:
        raise Http404
    except BlogEntryPage.MultipleObjectsReturned:
        raise Http404
    return entry.render_to_response(request)
