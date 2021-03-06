# Generated by Django 2.2.5 on 2020-12-20 07:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('otomobil', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otomobil',
            old_name='day',
            new_name='big_baggage',
        ),
        migrations.AddField(
            model_name='otomobil',
            name='abs',
            field=models.CharField(choices=[('True', 'Evet'), ('False', 'Hayır')], default='False', max_length=10),
        ),
        migrations.AddField(
            model_name='otomobil',
            name='daily_km',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='otomobil',
            name='driver_airbag',
            field=models.CharField(choices=[('True', 'Evet'), ('False', 'Hayır')], default='True', max_length=10),
        ),
        migrations.AddField(
            model_name='otomobil',
            name='min_age',
            field=models.IntegerField(default=18),
        ),
        migrations.AddField(
            model_name='otomobil',
            name='min_cc',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='otomobil',
            name='min_li_age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='otomobil',
            name='min_person',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='otomobil',
            name='passenger_airbag',
            field=models.CharField(choices=[('True', 'Evet'), ('False', 'Hayır')], default='True', max_length=10),
        ),
        migrations.AddField(
            model_name='otomobil',
            name='small_baggage',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Kira',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rezdate', models.DateTimeField(auto_now_add=True)),
                ('reztime', models.DateTimeField(auto_now_add=True)),
                ('returndate', models.DateTimeField(auto_now_add=True)),
                ('returntime', models.DateTimeField(auto_now_add=True)),
                ('days', models.IntegerField(default=18)),
                ('price', models.IntegerField(default=18)),
                ('total', models.IntegerField(default=18)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('note', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('True', 'Evet'), ('False', 'Hayır')], default='False', max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('otomobil', models.ForeignKey(default='None', on_delete=django.db.models.deletion.CASCADE, to='otomobil.Otomobil')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
