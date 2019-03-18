from rest_framework import serializers
from questions.models import Question

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
    class Meta:
        model = Question
        fields = '__all__'

