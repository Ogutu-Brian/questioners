import uuid

from django.db import models

from users.models import User
from meetups.models import Meetup

# Create your models here.
class Question(models.Model):
    """
    Database Model for questions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    body = models.TextField()
    meetup = models.ForeignKey(Meetup, related_name='meetup', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # db_table = 'Questions'
        ordering = ['created_at',]

    def __str__(self):
        return self.title
