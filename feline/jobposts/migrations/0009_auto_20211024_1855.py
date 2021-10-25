# Generated by Django 3.1.13 on 2021-10-24 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobposts', '0008_auto_20211017_0032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobpost',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='company',
            name='company_size',
            field=models.CharField(choices=[('Menos de 10', 'Micro'), ('10-50 Empleados', 'Small'), ('50-500 Empleados', 'Medium'), ('500-2000 Empleados', 'Large'), ('+2000 Empleados', 'X Large')], default='Menos de 10', max_length=20),
        ),
        migrations.AddField(
            model_name='company',
            name='tagline',
            field=models.CharField(blank=True, max_length=350, null=True, verbose_name='Slogan de la compañía'),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='currency',
            field=models.CharField(blank=True, choices=[('DOP', 'Pesos'), ('USD', 'Dollars'), ('EUR', 'Euros')], max_length=20, null=True),
        ),
    ]
