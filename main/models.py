# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from utils import generate_unique_key


class Profile(models.Model):

    GENDER_CHOICES = (
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    )

    user = models.OneToOneField(User)
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    birth_day = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    country = models.CharField(max_length=20, null=True, blank=True)
    created_on = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.user.email


class Offer(models.Model):

    name = models.TextField()
    description = models.TextField()
    discount_percent = models.IntegerField(null=True, blank=True)
    flat_discount = models.IntegerField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Store(models.Model):

    associated_brand = models.CharField(max_length=40)
    location = models.TextField()
    city = models.CharField(max_length=20)
    offers = models.ManyToManyField(Offer)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.associated_brand + " | " + self.city


class Brand(models.Model):

    name = models.CharField(max_length=20)
    stores = models.ManyToManyField(Store)
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.name


class Otp(models.Model):

    user = models.ForeignKey(User)
    otp = models.CharField(max_length=20)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.otp

    @classmethod
    def generate(cls, user):
        otp = cls.objects.create(
            user=user,
            otp=generate_unique_key(6)
        )
        return otp.otp


class EmailTemplate(models.Model):

    EMAIL_TYPE_CHOICES = (
        ('welcome-email', 'welcome-email'),
        ('forgot-password', 'forgot-password'),
        ('payment-success', 'payment-success'),
    )

    type = models.CharField(max_length=100, choices=EMAIL_TYPE_CHOICES, blank=True, null=True)
    subject = models.CharField(max_length=20, blank=True, null=True)
    body = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.type
