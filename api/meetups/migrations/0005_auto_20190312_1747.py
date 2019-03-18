# Generated by Django 2.1.7 on 2019-03-12 17:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meetups', '0004_auto_20190312_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='rsvp',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rsvp',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
