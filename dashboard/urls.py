from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("map/", views.DashboardView.as_view(), name="map"),
    path("stream/", views.stream, name="stream"),
]