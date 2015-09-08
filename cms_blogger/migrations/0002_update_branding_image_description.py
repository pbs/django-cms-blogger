# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms_blogger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='branding_image',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='filer.Image', help_text='Upload or select an image that appears behind the Blog Title and Blog Tagline at the top of all blog pages. Size: 960 pixels wide and no more than 150 pixels tall. <img width=700 src=/s/admin/img/blog-banner-help.jpg>', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='homeblog',
            name='branding_image',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='filer.Image', help_text='Upload or select an image that appears behind the Blog Title and Blog Tagline at the top of all blog pages. Size: 960 pixels wide and no more than 150 pixels tall. <img width=700 src=/s/admin/img/blog-banner-help.jpg>', null=True),
            preserve_default=True,
        ),
    ]
