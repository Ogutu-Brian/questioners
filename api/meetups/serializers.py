from rest_framework import serializers
from .models import Meetup, Tag


class MeetupSerializer(serializers.ModelSerializer):
    """
    Serializers for Meetup models
    """
    class Meta:
        model = Meetup
        fields = ('title', 'body', 'location', 'scheduled_date')


class TagSerializer(serializers.ModelSerializer):
    """
    Serializers for meetup tags (Tag Model)
    """
    class Meta:
        model = Tag
        fields = '__all__'
