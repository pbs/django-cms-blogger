# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from django.core import paginator
from django.db.models import Q
from cms_blogger.models import (
    BlogEntryPage,
    BlogCategory,
    BioPage,
    Blog,
    HomeBlog,
)
import itertools
import datetime


class BloggerSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        # Blogs, BlogRelatedPages, BlogEntryPages
        current_site = Site.objects.get_current()
        home_blog = HomeBlog.objects.filter(site=current_site)[:1]
        blog_current_site = Q(blog__site=current_site)
        blogs = Blog.objects.filter(site=current_site)
        # bio_pages = BioPage.objects.filter(blog_current_site)
        entry_pages = self.get_blog_entries(current_site)
        blog_categories = BlogCategory.objects.filter(blog_current_site)
        chained = itertools.chain(
            home_blog,
            blogs,
            # bio_pages.select_related('blog'),
            entry_pages,
            blog_categories.select_related('blog'),
        )
        return list(chained)

    def get_blog_entries(self, current_site):
        """
        Returns the queryset (preferably unevaluated) of blog entries that
        should be available in the sitemap.
        :param current_site: the site for which the sitemap is constructed
        """
        return (BlogEntryPage.objects.published().select_related('blog')
                .filter(blog__site=current_site))

    def lastmod(self, blog_related_object):
        latest = blog_related_object.modified_at
        return latest
