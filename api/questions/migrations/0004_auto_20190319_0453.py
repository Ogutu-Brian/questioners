# Generated by Django 2.1.7 on 2019-03-19 04:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0003_auto_20190319_0043'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='questionvote',
            unique_together={('vote', 'question', 'user')},
        ),
    ]
