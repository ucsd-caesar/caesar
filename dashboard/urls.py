from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path('search/', views.SearchView.as_view(), name='search'),
    path("stream/", views.StreamView.as_view(), name="stream"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("stop_stream/", views.StopStreamView.as_view(), name="stop_stream"),
    path("agency/<int:pk>/", views.AgencyView.as_view(), name="agency_homepage"),
    path("user/<int:pk>/", views.UserView.as_view(), name="user"),
    path("viewport/<int:user_id>/<int:viewport_id>/", views.ViewportView.as_view(), name="viewport"),
    path("agency/<int:agency_id>/invite", views.invite_user, name="invite_user"),
    path("viewport/post_viewport/", views.post_viewport, name="post_viewport"),
]