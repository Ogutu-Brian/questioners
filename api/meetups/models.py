from django.db import models
from users.models import User
import uuid
import datetime
"""
Models for the meetups
"""


class Tag(models.Model):
    """
    Database Model for meetup tags
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('tag_name',)

    def __str__(self):
        return self.tag_name

    def get_tag_name(self) -> str:
        """
        Returns tag name of the object
        """
        return self.tag_name


class Image(models.Model):
    """
    Database model for image urls for tags
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_url = models.URLField(max_length=255)

    class Meta:
        unique_together = ('image_url',)

    def __str__(self):
        return self.image_url

    def get_image_url(self) -> str:
        """
        Returns the image url
        """
        return self.image_url


class Meetup(models.Model):
    """
    Database Model for Meetups
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    location = models.CharField(max_length=255)
    scheduled_date = models.DateTimeField()
    tags = models.ManyToManyField(Tag)
    image_url = models.ManyToManyField(Image)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['scheduled_date', '-created_on']
        unique_together = (('body', 'scheduled_date', 'location'),
                           ('title', 'scheduled_date', 'location'))

    def __str__(self):
        return self.title + " on "+self.scheduled_date.strftime('%m-%d-%Y')
