# Generated by Django 3.1.13 on 2021-10-17 04:32

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobposts', '0007_auto_20211016_2345'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='is_remote',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_url',
            field=models.URLField(blank=True, verbose_name='Pagina de la Compañía'),
        ),
        migrations.AlterField(
            model_name='company',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, verbose_name='País'),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Logo de la Compañía'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nombre de la Compañía'),
        ),
    ]