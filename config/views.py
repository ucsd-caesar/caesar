from django.contrib.auth import views as auth_views
from django.urls import reverse
from dashboard.models import CustomUser

class LoginView(auth_views.LoginView):
    model = CustomUser
    template_name = "dashboard/login.html"

    def get_success_url(self):
        # redirect to /dashboard/
        return reverse('dashboard:dashboard')