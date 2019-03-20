from rest_framework import serializers
from questions.models import Question
from users.models import User
from users.serializers import FetchUserSerializer


class QuestionsSerializer(serializers.ModelSerializer):
    """
    serializer for Question model
    """
    class Meta:
        model = Question
        fields = (
            'title', 'body'
        )


class ViewQuestionsSerializer(serializers.ModelSerializer):
    """
    Serializer class for fetching all questions specific to that meetup
    """
    created_by = FetchUserSerializer()
    class Meta:
        model = Question
        fields = '__all__'
