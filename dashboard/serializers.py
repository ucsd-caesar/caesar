from rest_framework_gis import serializers
from .models import *

class MarkerSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = Marker
        geo_field = "location"
        fields = ("id", "name")

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ("name","members")

class LivestreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livestream
        fields = ("id", "title", "source", "agency", "created_by")

class CustomUserSerializer(serializers.ModelSerializer):
    created_livestreams = LivestreamSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ("username", "email", "is_admin", "created_livestreams")

class ViewportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewport
        fields = ("id", "user", "livestreams", "date_created", "time_created")