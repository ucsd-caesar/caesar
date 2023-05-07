from django import forms
from .models import CustomUser, Agency

class InviteUserForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email does not exist.")
        return email
    
class SRTLinkForm(forms.Form):
    title = forms.CharField(label='Title', required=True)
    srt_link = forms.URLField(
        label='SRT Link',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter SRT video streaming server link'})
    )
    agency = forms.ModelChoiceField(Agency.objects.all(), required=True)