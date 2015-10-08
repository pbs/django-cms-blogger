# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms_blogger', '0003_auto_20150929_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='riverplugin',
            name='entries_ordering',
            field=models.CharField(default=b'-update_date,slug', help_text='Blog entries ordering', max_length=255, choices=[(b'-update_date,slug', b'List blog entries by last updated'), (b'-update_date,slug', b'List blog entries by last published')]),
        ),
    ]
