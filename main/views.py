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
from django.db.models import Sum, Max


class SignupView(CreateAPIView):

    serializer_class = serializers.SignupSerializer
    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):

        if request.data.get('password') != request.data.get('confirm_password'):
            return Response(data={'error': 'Password mismatch'}, status=status.HTTP_200_OK, content_type="application/json")

        if models.User.objects.filter(email=request.data.get('email')).first() is not None:
            return Response(data={'error': 'User with this email already exists'}, status=status.HTTP_200_OK, content_type="application/json")

        user_obj = models.User.objects.create(
            email=request.data.get('email'),
            username=request.data.get('email')
        )
        user_obj.set_password(request.data.get('password'))
        user_obj.save()

        return Response(data={'success': 'Created'}, status=status.HTTP_201_CREATED, content_type="application/json")


class SendResetOtpView(GenericAPIView):

    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):

        user_obj = models.User.objects.filter(email=request.data['email']).first()

        if user_obj is None:
            return Response(data={'error': 'No user found'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, content_type="application/json")
        else:
            otp = models.Otp.generate(user_obj)
            return Response(data={'success': 'Otp sent on email','user': user_obj.email}, status=status.HTTP_200_OK, content_type="application/json")


class CheckOtpView(GenericAPIView):

    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):

        otp = request.data['otp']
        user_obj = models.User.objects.filter(email=request.data['email']).first()

        if models.Otp.objects.filter(user=user_obj).last().otp != otp:
            return Response(data={'error':'Wrong Otp'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, content_type="application/json")

        else:
            return Response(data={'success':'Allow reset','user': user_obj.email}, status=status.HTTP_200_OK, content_type="application/json")


class ResetPasswordView(GenericAPIView):

    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):

        password = request.data['password']
        confirm_password = request.data['confirm_password']

        if password != confirm_password:
            return Response(data={'error': 'Password mismatch'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, content_type="application/json")

        else:
            user_obj = models.User.objects.filter(email=request.data['email']).first()
            user_obj.set_password(confirm_password)
            user_obj.save()
            return Response(data={'success':'Password has been reset'}, status=status.HTTP_200_OK, content_type="application/json")


class DashboardBaseView(GenericAPIView):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):

        stats = dict()
        user_object = models.User.objects.get(username=request.user)
        offer_view_object = models.OfferViews.objects.filter(store__brand__owner=user_object,
                                                             store__subscribed=True,
                                                             offer__active=True
                                                             )

        stats['active_offers_count'] = models.Offer.objects.filter(store__brand__owner=user_object,
                                                                   store__subscribed=True,
                                                                   active=True).count()
        stats['active_stores_count'] = models.Store.objects.filter(brand__owner=user_object,
                                                                   subscribed=True).count()
        stats['total_views_offers'] = offer_view_object.aggregate(Sum('views'))['views__sum']
        stats['most_viewed_offer'] = models.OfferViews.objects.filter(views=offer_view_object.aggregate(Max('views'))['views__max']).first().offer.name
        stats['most_views_on'] = offer_view_object.aggregate(Max('views'))['views__max']

        print stats

        return Response(data=stats, status=status.HTTP_200_OK, content_type="application/json")
