# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, \
    GenericAPIView
from main import models, serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class SignupView(CreateAPIView):

    serializer_class = serializers.SignupSerializer
    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):

        if request.data.get('password') != request.data.get('confirm_password'):
            return Response(data={'error':'Password mismatch'}, status=status.HTTP_200_OK, content_type="application/json")

        if models.User.objects.filter(email=request.data.get('email')).first() is not None:
            return Response(data={'error':'User with this email already exists'}, status=status.HTTP_200_OK, content_type="application/json")

        user_obj = models.User.objects.create(
            email=request.data.get('email'),
            username=request.data.get('email')
        )
        user_obj.set_password(request.data.get('password'))
        user_obj.save()

        return Response(data={'success':'Created'}, status=status.HTTP_201_CREATED, content_type="application/json")


class ForgotPasswordView(GenericAPIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):

        user_obj = models.User.objects.filter(email=request.data['email']).first()

        if user_obj is None:
            return Response(data={'error':'No user found'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, content_type="application/json")

        pass
