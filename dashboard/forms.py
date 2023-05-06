from django import forms
from django.contrib.auth.models import User

class InviteUserForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email does not exist.")
        return email