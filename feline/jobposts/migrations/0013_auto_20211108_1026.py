# Generated by Django 3.1.13 on 2021-11-08 14:26

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobposts', '0012_auto_20211103_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='how_to_apply',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
