# Generated by Django 3.0.2 on 2020-02-03 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GeoInfoSystem', '0004_puntinteres_pais'),
    ]

    operations = [
        migrations.RenameField(
            model_name='puntinteres',
            old_name='logitud',
            new_name='longitud',
        ),
    ]