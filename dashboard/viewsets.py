from rest_framework import viewsets
from rest_framework import generics
from rest_framework_gis import filters

from .models import *
from .serializers import *

class MarkerViewSet(viewsets.ModelViewSet):
    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class LivestreamViewSet(viewsets.ModelViewSet):
    queryset = Livestream.objects.all()
    serializer_class = LivestreamSerializer

class ViewportViewSet(viewsets.ModelViewSet):
    queryset = Viewport.objects.all()
    serializer_class = ViewportSerializer