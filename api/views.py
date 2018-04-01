# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password, make_password


@api_view(['POST'])
def user_register(request):
    username = request.data['username']
    password = request.data['password']
    first_name = request.data['firstName']
    last_name = request.data['lastName']

    user = User.objects.filter(username=username).first()

    if user:
        return Response({"message": "Username already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        hashed_password = make_password(password)
        User.objects.create(username=username, password=hashed_password, first_name=first_name, last_name=last_name)

        return Response({"message": "User successfully registered"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def admin_register(request):
    username = request.data['username']
    password = request.data['password']
    first_name = request.data['firstName']
    last_name = request.data['lastName']

    user = Admin.objects.filter(username=username).first()

    if user:
        return Response({"message": "Username already Exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        hashed_password = make_password(password)
        Admin.objects.create(username=username, password=hashed_password, first_name=first_name, last_name=last_name)

        return Response({"message": "User Successfully Registered"}, status=status.HTTP_201_CREATED)
