from rest_framework import serializers
from .models import WebsiteData


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteData
        fields = ('url', 'no_of_visitors', 'total_usage_hours', 'no_of_hits', 'last_visited')
