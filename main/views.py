# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from main import models, serializers
from rest_framework import status
from rest_framework.response import Response


class SignupView(CreateAPIView):

    serializer_class = serializers.SignupSerializer

    def create(self, request, *args, **kwargs):

        if request.data.get('password') != request.data.get('confirm_password'):
            return Response(data={'error':'Password mismatch'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        if models.User.objects.filter(email=request.data.get('email')).first() is None:
            return Response(data={'error':'User already created with this email id'}, status=status.HTTP_302_FOUND)

        user_obj = models.User.objects.create(
            username=request.data.get('email'),
            email=request.data.get('email')
        )
        user_obj.set_password(request.data.get('password'))

        return Response(data={'success':'Created'}, status=status.HTTP_201_CREATED)

