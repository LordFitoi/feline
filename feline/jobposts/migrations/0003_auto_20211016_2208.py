# Generated by Django 3.1.13 on 2021-10-17 02:08

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobposts', '0002_insert_category_default_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
