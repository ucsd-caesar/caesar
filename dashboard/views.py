from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from django.views.generic.base import TemplateView
from dotenv import load_dotenv
from json import JSONDecodeError
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response
from .models import *
from .serializers import *

import os

load_dotenv() # load environment variables from .env file

class DashboardView(generic.ListView):
    model = MapChoice
    template_name = "dashboard/map.html"
    context_object_name = "map_choices"
    
    def get_queryset(self):
        return MapChoice.objects.all()
    
def stream(request):
    return render(request, 'dashboard/stream.html')

class LoginView(TemplateView):
    template_name = "dashboard/login.html"

class UserAPIView(views.APIView):
    serializer_class = UserSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
            }
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    
    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = UserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)