# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    GENDER_CHOICES = (
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    )

    user = models.OneToOneField(User)
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    birth_day = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    country = models.CharField(max_length=20, null=True, blank=True)
    created_on = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.user.email


class Department(models.Model):

    name = models.CharField(max_length=40)
    created_on = models.DateField(auto_now_add=True,editable=False)

    def __str__(self):
        return self.name


class Employee(models.Model):

    user = models.ForeignKey(Profile)
    department = models.ForeignKey(Department)
    salary = models.CharField(max_length=20)
    role = models.CharField(max_length=40)
    joining = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " | " + str(self.role)


class Project(models.Model):

    PHASES = (
        ('Planning','Planning'),
        ('Designing','Designing'),
        ('Development','Development'),
        ('Testing','Testing'),
        ('Completed','Completed'),
        ('Delivered','Delivered')
    )

    name = models.CharField(max_length=20)
    team = models.ManyToManyField(Employee)
    start_date = models.DateField(auto_now_add=True, editable=False)
    delivery_date = models.DateField()
    phase = models.CharField(choices=PHASES, max_length=20)

    def __str__(self):
        return str(self.name) + " | " + str(self.phase)
