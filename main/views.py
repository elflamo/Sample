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


class LoginView(GenericAPIView):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        print request.user

        if request.user:
            return Response(data={'success':True}, status=status.HTTP_200_OK)
        else:
            return Response(data={'success':False}, status=status.HTTP_404_NOT_FOUND)
