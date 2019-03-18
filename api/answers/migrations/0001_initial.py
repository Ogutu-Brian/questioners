# Generated by Django 2.1.7 on 2019-03-18 14:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created_on', models.DateTimeField(auto_now_add=True)),
                ('date_updated_on', models.DateTimeField(auto_now=True)),
                ('body', models.TextField()),
            ],
            options={
                'ordering': ['-date_created_on'],
            },
        ),
    ]