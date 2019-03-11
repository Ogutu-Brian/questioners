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