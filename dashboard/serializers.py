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
        fields = ("name",)

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "is_admin", "livestreams")

class LivestreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livestream
        fields = ("title", "source", "agency", "created_by")