from rest_framework import serializers
from .models import Meetup, Tag
from django.utils import timezone


class MeetupSerializer(serializers.ModelSerializer):
    """
    Serializers for Meetup models
    """
    class Meta:
        model = Meetup
        fields = ('title', 'body', 'location', 'scheduled_date')

    def validate(self, data):
        """
        Check if a meetup was scheduled on a past date
        """
        scheduled_date = data.get('scheduled_date')
        if scheduled_date < timezone.now():
            raise serializers.ValidationError(
                'You cannot schedule a meetup on a past time')
        return data


class TagSerializer(serializers.ModelSerializer):
    """
    Serializers for meetup tags (Tag Model)
    """
    class Meta:
        model = Tag
        fields = '__all__'


class FetchMeetupSerializer(serializers.ModelSerializer):
    """
    Serializes all the data from fields
    """
    tags = serializers.StringRelatedField(many=True)
    image_url = serializers.StringRelatedField(many=True)

    class Meta:
        model = Meetup
        fields = '__all__'


class UpdateMeetupSerializer(serializers.ModelSerializer):
    """
    Serializer for updating meetups
    """
    tags = serializers.StringRelatedField(many=True)
    image_url = serializers.StringRelatedField(many=True)

    class Meta:
        model = Meetup
        fields = '__all__'
