# Generated by Django 3.1.13 on 2021-11-03 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobposts', '0010_auto_20211024_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
