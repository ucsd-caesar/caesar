from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("map/", views.DashboardView.as_view(), name="map"),
    path("stream/", views.stream, name="stream"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("user/", views.UserAPIView.as_view()),
    path("agency/<int:pk>/", views.AgencyView.as_view(), name="agency_homepage"),
    path("user/<int:user_id>/", views.UserView.as_view(), name="user_homepage"),
    path("agency/<int:agency_id>/invite", views.invite_user, name="invite_user"),
]