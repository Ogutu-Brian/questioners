from rest_framework import serializers
from .models import User


class FetchUserSerializer(serializers.ModelSerializer):
    """
    Serializer for fetching user data
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'nick_name')
