from django.shortcuts import render
from django.views import generic
from django.views.generic.base import TemplateView
from dotenv import load_dotenv
from rest_framework.response import Response
from .models import *
from .serializers import *

import os

load_dotenv() # load environment variables from .env file

class DashboardView(generic.ListView):
    model = Camera
    template_name = "dashboard/map.html"
    context_object_name = "cameras"
    
    def get_queryset(self):
        return Camera.objects.all()
    