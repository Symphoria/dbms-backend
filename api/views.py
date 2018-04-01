# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password, make_password
from .permissions import *
from .serializers import *
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


class AdminWebsiteView(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request):
        admin = request.admin
        websites_urls = AdminWebsite.objects.filter(admin_username=admin).values_list('website_url', flat=True)

        if len(websites_urls) > 0:
            website_data = WebsiteData.objects.filter(url__in=websites_urls)
            website_payload = WebsiteSerializer(website_data, many=True).data

            return Response(website_payload, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Websites Added"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        admin = request.admin
        website_url = request.data['websiteUrl']

        website_exists = WebsiteData.objects.filter(url=website_url).exists()

        if not website_exists:
            website = WebsiteData.objects.create(url=website_url)
        else:
            website = WebsiteData.objects.filter(url=website_url).first()

        admin_website_exists = AdminWebsite.objects.filter(admin_username=admin, website_url=website).exists()

        if not admin_website_exists:
            AdminWebsite.objects.create(admin_username=admin, website_url=website)

            return Response({"message": "Website Added"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Website already added"}, status=status.HTTP_400_BAD_REQUEST)


class UserWebsiteView(APIView):
    permission_classes = (IsUser,)


@api_view(['GET'])
def get_log(request):
    visitors = int(request.GET.get('visitors'))
    website_url = request.GET.get('link')
    total_time = float(request.GET.get('time'))

    website = WebsiteData.objects.filter(url=website_url).first()

    if website:
        website.no_of_visitors += visitors
        website.no_of_hits += 1
        website.total_usage_hours += total_time
        website.save()
    else:
        WebsiteData.objects.create(url=website_url, no_of_visitors=1, total_usage_hours=total_time, no_of_hits=1)

    return Response("Success", status=status.HTTP_200_OK)
