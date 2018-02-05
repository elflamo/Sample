from rest_framework import serializers
from main import models

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=10)
    password = serializers.CharField(max_length=20)
    confirm_password = serializers.CharField(max_length=20)


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = models.User
