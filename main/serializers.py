from rest_framework import serializers
from main import models

class SignupSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=20, required=True)
    password = serializers.CharField(max_length=20, required=True)
    confirm_password = serializers.CharField(max_length=20, required=True)

class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=20, required=True)
