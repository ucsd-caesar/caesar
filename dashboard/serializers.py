from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import *

class MarkerSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Marker
        geo_field = "location"
        fields = ("id", "name")

class LivestreamSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all(),
        required=False
    )
    created_by = serializers.SerializerMethodField()
    created_by_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='created_by')

    class Meta:
        model = Livestream
        fields = ("id", "title", "source", "groups", "created_by", "created_by_id")
    
    def get_created_by(self, obj):
        return obj.created_by.username
    
    def get_groups(self, obj):
        return [group.name for group in obj.groups.all()]
    
    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        instance = super().create(validated_data)

        # if no groups are specified, add Public group
        if groups is not None and len(groups) == 0:
            instance.groups.add(Group.objects.get(name='Public'))
        else:
            for group in groups:
                instance.groups.add(group)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', [])
        instance = super().update(instance, validated_data)
        for group in groups:
            instance.groups.add(group)
        instance.save()
        return instance


class CustomUserSerializer(serializers.ModelSerializer):
    created_livestreams = LivestreamSerializer(many=True, read_only=True)
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all(),
        required=False
    )
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password", "is_admin", "groups", "created_livestreams", "viewports")
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

class GroupSerializer(serializers.ModelSerializer):
    members = CustomUserSerializer(many=True, read_only=True, source='user_set')
    class Meta:
        model = Group
        fields = ("id", "name", "permissions", "members")