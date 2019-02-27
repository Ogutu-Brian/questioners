"""
Models for the answers
"""
import uuid
import datetime

from django.db import models
from users.models import User
from questions.models import Question


class Answer(models.Model):
    """
    Database Model for Answer
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created_on = models.DateTimeField(auto_now_add=True)
    date_updated_on = models.DateTimeField(auto_now=True)
    body = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_created_on']

    def __str__(self):
        return self.body + " on " + self.date_created_on.strftime('%m-%d-%Y')
