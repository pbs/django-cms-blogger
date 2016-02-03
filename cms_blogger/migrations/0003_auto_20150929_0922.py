# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms_blogger', '0002_update_branding_image_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='branding_image',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, default=None, to='filer.Image', blank=True, help_text='Blog Branding Image', null=True, verbose_name='Branding Image'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='disable_disqus_for_mobile',
            field=models.BooleanField(default=False, help_text='Select ON to hide comments on phone sized mobile devices.', verbose_name='DISABLE Disqus commenting at mobile breakpoints (<480)'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='disqus_shortname',
            field=models.CharField(help_text='Blog Disqus Shortname', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='email_account_link',
            field=models.BooleanField(default=True, help_text='Blog Email integration'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='enable_facebook',
            field=models.BooleanField(default=True, help_text='Blog Facebook integration', verbose_name='Facebook integration'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='enable_twitter',
            field=models.BooleanField(default=True, help_text='Blog Twitter integration', verbose_name='Twitter integration'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='entries_slugs_with_date',
            field=models.BooleanField(default=False, help_text='Blog Entries With Slugs', verbose_name='Dates in blog entry URLs'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='in_navigation',
            field=models.BooleanField(default=False, help_text='Blog navigation', verbose_name='Add blog to navigation'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='site',
            field=models.ForeignKey(verbose_name='site', to='sites.Site', help_text='Blog Site'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(help_text='Blog Slug', verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='tagline',
            field=models.CharField(help_text='Blog Tagline', max_length=70, null=True, verbose_name='tagline', blank=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(help_text='Blog Title', max_length=50, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='homeblog',
            name='branding_image',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, default=None, to='filer.Image', blank=True, help_text='Blog Branding Image', null=True, verbose_name='Branding Image'),
        ),
        migrations.AlterField(
            model_name='homeblog',
            name='in_navigation',
            field=models.BooleanField(default=False, help_text='Blog navigation', verbose_name='Add blog to navigation'),
        ),
        migrations.AlterField(
            model_name='homeblog',
            name='site',
            field=models.ForeignKey(verbose_name='site', to='sites.Site', help_text='Blog Site'),
        ),
        migrations.AlterField(
            model_name='homeblog',
            name='tagline',
            field=models.CharField(help_text='Blog Tagline', max_length=70, null=True, verbose_name='tagline', blank=True),
        ),
        migrations.AlterField(
            model_name='homeblog',
            name='title',
            field=models.CharField(help_text='Blog Title', max_length=50, verbose_name='title'),
        ),
    ]
