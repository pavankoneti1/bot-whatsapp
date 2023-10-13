from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import User

class UserSerializer(ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "mobile_number", "token"]

    def get_token(self, user):
        return user.auth_token.key