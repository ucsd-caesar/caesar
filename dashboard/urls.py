from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path('search/', views.SearchView.as_view(), name='search'),
    path("login/", views.LoginView.as_view(), name="login"),

    path("user/<int:pk>/", views.UserView.as_view(), name="user"),
    path("user/<int:livestream_id>/delete/", views.UserView.stop_stream, name="stop_stream"),
    path("change-visibility/<int:livestream_id>/", views.UserView.as_view(), name="change_visibility"),
    path("stream/", views.StreamView.as_view(), name="stream"),
    path("auth_stream/", views.auth_stream, name="auth_stream"),

    path("group/<int:pk>/", views.GroupView.as_view(), name="group_homepage"),
    path("group/<int:group_id>/invite", views.GroupView.invite_user, name="invite_user"),

    path("viewport/<int:user_id>/<int:viewport_id>/", views.ViewportView.as_view(), name="viewport"),
    path("viewport/post_viewport/", views.ViewportView.post, name="post_viewport"),
    path("viewport/<int:viewport_id>/delete/", views.ViewportView.delete, name="delete"),
]