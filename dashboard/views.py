from django.shortcuts import render
from django.views.generic.base import TemplateView
from config.settings import MAPBOX_API_KEY


class DashboardView(TemplateView):
    template_name = "dashboard/map.html"
