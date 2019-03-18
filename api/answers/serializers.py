"""
Serializers for the amswers model
"""

from rest_framework import serializers
from .models import Answer
from django.utils import timezone


class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializers for Answer models
    """
    class Meta:
        model = Answer
        fields = ('body',)
