# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import django.utils.timezone
import cms_blogger.models
import cms.models.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
        ('filer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('slug', models.SlugField(help_text="Used to build the author's URL.", unique=True, max_length=150, verbose_name='slug')),
                ('user', models.ForeignKey(related_name='blog_authors', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BioPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('author', models.ForeignKey(to='cms_blogger.Author')),
            ],
            options={
            },
            bases=(models.Model, cms_blogger.models.BlogRelatedPage),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text="Please enter the blog's title. This title will be displayed at the top of all blog-related pages, above the Blog Tagline, and on top of the Blog Branding Image (if one is used). Ideally, it should be no longer than 30 characters.", max_length=50, verbose_name='title')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('tagline', models.CharField(help_text='Optional. Appears immediately below the Blog Title, and over the Blog Branding Image (if one is used). Recommended: 60 characters or fewer.', max_length=70, null=True, verbose_name='Blog Tagline', blank=True)),
                ('in_navigation', models.BooleanField(default=False, help_text='ON allows users to display this blog in the navigation menu.', verbose_name='Add blog to navigation')),
                ('slug', models.SlugField(help_text='The blog slug is the URL for the blog landing page, and will be present in ALL blog entry URLs. It is best to use a slug no more than 25 characters. It may not contain spaces or special characters.', verbose_name='slug')),
                ('entries_slugs_with_date', models.BooleanField(default=False, help_text='Blogs that are frequently updated, especially news-themed blogs, often insert dates [/2014/03/15/] into the URLs for blog entries. To insert a date-stamp into all blog entries for this blog, select ON.', verbose_name='Insert dates into blog entry URLs')),
                ('enable_facebook', models.BooleanField(default=True, help_text='ON allows users to share blog entries on Facebook. The post will pull the Open Graph information from the blog entry metadata.', verbose_name='Facebook integration')),
                ('enable_twitter', models.BooleanField(default=True, help_text='ON allows users to share blog entries via Twitter. The Tweet will derive information from the blog entry metadata.', verbose_name='Twitter integration')),
                ('email_account_link', models.BooleanField(default=True, help_text="ON allows users to email the post's short description and a link to it.")),
                ('enable_disqus', models.BooleanField(default=False)),
                ('disqus_shortname', models.CharField(help_text='Tells Disqus which website account (called a forum on Disqus) this system belongs to.', max_length=255, null=True, blank=True)),
                ('disable_disqus_for_mobile', models.BooleanField(default=False, help_text='Selecting ON hides comments on phone-sized mobile devices. This improves page load speed and prevents hanging issues for users relying on cellular data service.', verbose_name='DISABLE Disqus commenting at mobile breakpoints (<480)')),
                ('allowed_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Add Users')),
                ('branding_image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='filer.Image', help_text="Upload or select an image that appears behind the Blog Title and Blog Tagline at the top of all blog pages. Size: 960 pixels wide and no more than 150 pixels tall. <span class='help-tooltip' title='<img width=700 src=STATIC_URLadmin/img/blog-banner-help.jpg>'>What's this?</span>", null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name', db_index=True)),
                ('slug', models.SlugField(max_length=30, verbose_name='slug')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('blog', models.ForeignKey(related_name='categories', to='cms_blogger.Blog')),
            ],
            options={
            },
            bases=(models.Model, cms_blogger.models.BlogRelatedPage),
        ),
        migrations.CreateModel(
            name='BlogEntryPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(help_text="Used to build the entry's URL.", max_length=255, verbose_name='slug')),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now, help_text="Used to build the entry's URL.", verbose_name='publication date', db_index=True)),
                ('poster_image', models.ImageField(upload_to=cms_blogger.models.upload_entry_image, verbose_name='Thumbnail Image', blank=True)),
                ('caption', models.CharField(max_length=70, null=True, verbose_name='caption', blank=True)),
                ('credit', models.CharField(max_length=35, null=True, verbose_name='credit', blank=True)),
                ('short_description', models.TextField(help_text='400 characters or fewer', max_length=400, verbose_name='Short Description')),
                ('start_publication', models.DateTimeField(help_text='Start date of publication.', null=True, verbose_name='start publication', db_index=True, blank=True)),
                ('end_publication', models.DateTimeField(help_text='End date of publication.', null=True, verbose_name='end publication', db_index=True, blank=True)),
                ('is_published', models.BooleanField(default=False, verbose_name='is published')),
                ('seo_title', models.CharField(max_length=120, verbose_name='SEO Title', blank=True)),
                ('meta_keywords', models.CharField(max_length=120, verbose_name='Keywords Meta', blank=True)),
                ('disqus_enabled', models.BooleanField(default=True, help_text='Set OFF to disable commenting for this entry.', verbose_name='Disqus integration')),
                ('enable_poster_image', models.BooleanField(default=True, help_text='Display thumbnail in blog entry', verbose_name='Display thumbnail')),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('draft_id', models.CharField(max_length=32, db_index=True)),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('authors', models.ManyToManyField(related_name='blog_entries', verbose_name='Blog Entry Authors', to='cms_blogger.Author')),
                ('blog', models.ForeignKey(to='cms_blogger.Blog')),
                ('content', cms.models.fields.PlaceholderField(to='cms.Placeholder', null=True, slotname=b'content')),
            ],
            options={
                'verbose_name': 'blog entry',
                'verbose_name_plural': 'blog entries',
            },
            bases=(models.Model, cms_blogger.models.BlogRelatedPage),
        ),
        migrations.CreateModel(
            name='BlogNavigationNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=15)),
                ('position', models.PositiveIntegerField()),
                ('parent_node_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HomeBlog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text="Please enter the blog's title. This title will be displayed at the top of all blog-related pages, above the Blog Tagline, and on top of the Blog Branding Image (if one is used). Ideally, it should be no longer than 30 characters.", max_length=50, verbose_name='title')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('tagline', models.CharField(help_text='Optional. Appears immediately below the Blog Title, and over the Blog Branding Image (if one is used). Recommended: 60 characters or fewer.', max_length=70, null=True, verbose_name='Blog Tagline', blank=True)),
                ('in_navigation', models.BooleanField(default=False, help_text='ON allows users to display this blog in the navigation menu.', verbose_name='Add blog to navigation')),
                ('branding_image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='filer.Image', help_text="Upload or select an image that appears behind the Blog Title and Blog Tagline at the top of all blog pages. Size: 960 pixels wide and no more than 150 pixels tall. <span class='help-tooltip' title='<img width=700 src=STATIC_URLadmin/img/blog-banner-help.jpg>'>What's this?</span>", null=True)),
                ('navigation_node', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cms_blogger.BlogNavigationNode', null=True)),
                ('site', models.ForeignKey(verbose_name='site', to='sites.Site', help_text='The site associated with this blog.')),
            ],
            options={
                'verbose_name': 'Super Landing Page',
                'verbose_name_plural': 'Super Landing Page',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RiverPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('categories', models.CharField(max_length=619, verbose_name=cms_blogger.models.BlogCategory)),
                ('display_abstract', models.BooleanField(default=True)),
                ('display_thumbnails', models.BooleanField(default=True)),
                ('paginate_entries', models.BooleanField(default=True)),
                ('number_of_entries', models.PositiveIntegerField(default=10, verbose_name='Entries to Display')),
            ],
            options={
                'db_table': 'cmsplugin_riverplugin',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterUniqueTogether(
            name='blogentrypage',
            unique_together=set([('slug', 'blog', 'draft_id')]),
        ),
        migrations.AddField(
            model_name='blogcategory',
            name='entries',
            field=models.ManyToManyField(related_name='categories', to='cms_blogger.BlogEntryPage'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='blogcategory',
            unique_together=set([('slug', 'blog')]),
        ),
        migrations.AddField(
            model_name='blog',
            name='navigation_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cms_blogger.BlogNavigationNode', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blog',
            name='site',
            field=models.ForeignKey(verbose_name='site', to='sites.Site', help_text='The site associated with this blog.'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='blog',
            unique_together=set([('slug', 'site')]),
        ),
        migrations.AddField(
            model_name='biopage',
            name='blog',
            field=models.ForeignKey(to='cms_blogger.Blog'),
            preserve_default=True,
        ),
    ]
