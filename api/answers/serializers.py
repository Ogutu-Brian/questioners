"""
Serializers for the amswers model
"""

from rest_framework import serializers
from .models import Answer, AnswerVote
from django.utils import timezone
from users.models import User
from users.serializers import FetchUserSerializer


class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializers for Answer models
    """
    votes = serializers.ReadOnlyField()

    class Meta:
        model = Answer
        fields = ('body', 'votes')


class VoteSerializer(serializers.ModelSerializer):
    """
    Model serializers for votes
    """
    class Meta:
        model = AnswerVote
        fields = '__all__'


class GetAnswerSerializer(serializers.ModelSerializer):
    """
    Serializers for Answer models
    """
    votes = serializers.ReadOnlyField()
    creator = FetchUserSerializer()

    class Meta:
        model = Answer
        fields = '__all__'
