# Generated by Django 3.0.2 on 2020-02-09 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeoInfoSystem', '0006_auto_20200204_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuari',
            name='alies',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]