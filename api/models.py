# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100, default=None)
    username = models.CharField(max_length=200, unique=True, primary_key=True)
    password = models.CharField(max_length=200)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class WebsiteData(models.Model):
    url = models.URLField(max_length=200, unique=True, primary_key=True)
    no_of_visitors = models.PositiveIntegerField(default=0)
    total_usage_hours = models.PositiveIntegerField(default=0)
    no_of_hits = models.PositiveIntegerField(default=0)
    last_visited = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'website_data'

    def __str__(self):
        return self.url


class Keywords(models.Model):
    website_url = models.ForeignKey(WebsiteData, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=150, default=None)

    class Meta:
        db_table = 'keywords'

    def __str__(self):
        return self.website_url.url + " " + self.keyword


class Admin(models.Model):
    username = models.CharField(max_length=200, unique=True, primary_key=True)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=150, default=None)
    last_name = models.CharField(max_length=150, default=None)

    class Meta:
        db_table = 'Admin'

    def __str__(self):
        return self.username


class AdminWebsite(models.Model):
    admin_username = models.ForeignKey(Admin, on_delete=models.CASCADE)
    website_url = models.ForeignKey(WebsiteData, on_delete=models.CASCADE)

    class Meta:
        db_table = 'admin_website'

    def __str__(self):
        return self.admin_username.username + " " + self.website_url.url
