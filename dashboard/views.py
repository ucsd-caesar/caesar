from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views import generic
from django.views.generic.base import TemplateView
from dotenv import load_dotenv
from .models import MapChoice
import os

load_dotenv() # load environment variables from .env file

class DashboardView(generic.ListView):
    model = MapChoice
    template_name = "dashboard/map.html"
    context_object_name = "map_choices"
    
    def get_queryset(self):
        return MapChoice.objects.all()
    