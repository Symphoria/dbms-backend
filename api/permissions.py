from rest_framework import permissions
from .models import Admin, User
import jwt
import os


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'HTTP_AUTHORIZATION_TOKEN' in request.META:
            jwt_token = request.META['HTTP_AUTHORIZATION_TOKEN']

            try:
                payload = jwt.decode(jwt_token, os.environ.get('JWT_SECRET'))
                print payload['user_type']
                print payload['username']
                if payload['user_type'] == "admin":
                    admin = Admin.objects.filter(username=payload['username']).first()

                    if admin:
                        request.admin = admin

                        return request

                return False
            except jwt.ExpiredSignatureError:
                return False
        else:
            return False
