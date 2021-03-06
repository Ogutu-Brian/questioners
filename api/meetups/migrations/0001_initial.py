
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image_url', models.URLField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Meetup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('scheduled_date', models.DateTimeField()),
            ],
            options={
                'ordering': ['scheduled_date', '-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Rsvp',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('response', models.CharField(max_length=5)),
                ('meetup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetups.Meetup')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tag_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together={('tag_name',)},
        ),
]