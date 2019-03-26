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

    @property
    def votes(self):
        upvotes = AnswerVote.objects.filter(answer=self.id,
                                            vote_type='upvote').count()
        downvotes = AnswerVote.objects.filter(answer=self.id,
                                              vote_type='downvote').count()
        votes = upvotes-downvotes
        resultset = {
            'upvotes': upvotes,
            'downvotes': downvotes,
            'vote_score': votes
        }
        return resultset

    def __str__(self):
        return self.body + " on " + self.date_created_on.strftime('%m-%d-%Y')


class AnswerVote(models.Model):
    """
    Voting for answers model
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    vote_type = models.TextField(default='none')

    class Meta:
        unique_together = ('creator', 'answer', 'vote_type')

    def __str__(self):
        return self.vote_type
