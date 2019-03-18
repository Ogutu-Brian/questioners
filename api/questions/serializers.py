from rest_framework import serializers
from questions.models import Question, QuestionVote
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


class VoteSerializer(serializers.ModelSerializer):
    """
    Mdel serializers for votes
    """
    class Meta:
        model = QuestionVote
        fields = '__all__'


class ViewQuestionsSerializer(serializers.ModelSerializer):
    """
    Serializer class for fetching all questions specific to that meetup
    """
    votes = serializers.ReadOnlyField()
    created_by = FetchUserSerializer()

    class Meta:
        model = Question
        fields = '__all__'
