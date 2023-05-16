from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import *

class MarkerSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Marker
        geo_field = "location"
        fields = ("id", "name")

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ("name","members")

class LivestreamSerializer(serializers.ModelSerializer):
    agency = serializers.StringRelatedField()
    created_by = serializers.SerializerMethodField()
    class Meta:
        model = Livestream
        fields = ("id", "title", "source", "agency", "created_by")

    def get_created_by(self, obj):
        return obj.created_by.username
    
    created_by = serializers.CurrentUserDefault()
    
    def post(self, instance, validated_data):
        instance.created_by_id = validated_data.get('created_by_id', None)
        instance.save()
        return instance

class CustomUserSerializer(serializers.ModelSerializer):
    created_livestreams = LivestreamSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password", "is_admin", "created_livestreams", "viewports")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        viewports = validated_data.pop('viewports', [])
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        for viewport in viewports:
            user.viewports.add(viewport)
        return user

class ViewportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewport
        fields = ("id", "name", "user", "livestreams", "date_created", "time_created")