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
    meetup = models.ForeignKey(
        Meetup, related_name='meetup', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # db_table = 'Questions'
        ordering = ['created_at', ]

    @property
    def votes(self):
        """
        Gets votes statistics specific to a question
        """
        upvotes = QuestionVote.objects.filter(
            question=self.id, vote__gte=1).count()
        downvotes = QuestionVote.objects.filter(
            question=self.id, vote__lt=1).count()
        votes = upvotes-downvotes
        resultset = {
            'upvotes': upvotes,
            'downvotes': downvotes,
            'vote_score': votes
        }
        return resultset

    def __str__(self):
        return self.title


class QuestionVote(models.Model):
    """
    Model for voting questions
    """
    VOTE_CHOICES = (
        (1, 'upvote'),
        (-1, 'downvote'),
    )
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    vote = models.IntegerField(choices=VOTE_CHOICES)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('vote', 'question', 'user')

    def __str__(self):
        return str(self.vote)
