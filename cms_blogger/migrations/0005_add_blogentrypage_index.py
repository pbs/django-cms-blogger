# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms_blogger', '0004_auto_20151009_1024'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='blogentrypage',
            index_together=set([('blog', 'is_published', 'publication_date')]),
        ),
    ]
