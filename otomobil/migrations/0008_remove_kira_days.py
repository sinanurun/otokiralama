# Generated by Django 2.2.5 on 2020-12-20 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('otomobil', '0007_auto_20201220_0919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kira',
            name='days',
        ),
    ]
