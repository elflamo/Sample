# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from main import models, serializers


class ListUsersView(ListAPIView):

    serializer_class = serializers.ListUserSerializer
    queryset = models.User.objects.all()