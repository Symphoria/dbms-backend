# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password, make_password
import jwt
import os
import json


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


@api_view(['POST'])
def user_login(request):
    username = request.data['username']
    password = request.data['password']

    user = User.objects.filter(username=username).first()

    if user:
        if check_password(password, user.password):
            jwt_payload = {
                "username": user.username,
                "user_type": "user",
                "exp": datetime.now() + timedelta(days=7)
            }
            auth_token = jwt.encode(jwt_payload, os.environ.get('JWT_SECRET'))
            payload = {
                "authToken": auth_token
            }

            return Response(json.dumps(payload), status=status.HTTP_200_OK)

    return Response({"message": "Username or password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def admin_login(request):
    username = request.data['username']
    password = request.data['password']

    admin = Admin.objects.filter(username=username).first()

    if admin:
        if check_password(password, admin.password):
            jwt_payload = {
                "username": admin.username,
                "user_type": "admin",
                "exp": datetime.now() + timedelta(days=7)
            }
            auth_token = jwt.encode(jwt_payload, os.environ.get('JWT_SECRET'))
            payload = {
                "authToken": auth_token
            }

            return Response(json.dumps(payload), status=status.HTTP_200_OK)

    return Response({"message": "Username or password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
