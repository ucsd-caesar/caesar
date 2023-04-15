from django.shortcuts import render
from django.views import generic
from .models import Dashboard

class DashboardView(generic.ListView):
    model = Dashboard
    template_name = 'dashboard/dashboard.html'

    def get_queryset(self):
        return Dashboard.objects.name
