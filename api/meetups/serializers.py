from .models import Meetup, Tag, Rsvp
from djoser import utils
from django.utils import timezone
from .models import Meetup, Tag
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from users.models import User
from users.serializers import FetchUserSerializer
from rest_framework import serializers

User = get_user_model()


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
    creator = FetchUserSerializer()
    rsvp_summary = serializers.ReadOnlyField()

    class Meta:
        model = Meetup
        fields = ('id', 'created_on', 'updated_on', 'title', 'body', 'location',
                  'scheduled_date', 'tags', 'image_url', 'creator', 'rsvp_summary')


class UpdateMeetupSerializer(serializers.ModelSerializer):
    """
    Serializer for updating meetups
    """
    tags = serializers.StringRelatedField(many=True)
    image_url = serializers.StringRelatedField(many=True)

    class Meta:
        model = Meetup
        fields = '__all__'


class RsvpSerializer(serializers.ModelSerializer):
    """
    Serializers for rsvp
    """
    response = serializers.CharField()

    def validate_response(self, value):
        """
        Validate User response
        """
        if "yes" not in value.lower():
            if "no" not in value.lower():
                if "maybe" not in value.lower():
                    raise serializers.ValidationError(
                        "RSVP, can only take Yes, No or Maybe")
        return value

    class Meta:
        model = Rsvp
        fields = ("id", "response", "created_on", "updated_on")


class FetchRsvpSerializer(serializers.ModelSerializer):
    """
    Serializer for fetching rsvp data
    """
    responder = FetchUserSerializer()

    class Meta:
        model = Rsvp
        fields = '__all__'
