# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2017-06-13 15:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20170613_1523'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='id',
            new_name='message_id',
        ),
    ]