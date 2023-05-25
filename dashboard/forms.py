from django import forms
from django.contrib.auth.models import Group
from .models import CustomUser, Livestream

class InviteUserForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email does not exist.")
        return email
    
class LivestreamVisibilityForm(forms.ModelForm):
    class Meta:
        model = Livestream
        fields = ('groups',)

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(), 
        widget=forms.CheckboxSelectMultiple,
        required=False)
    livestream_id = forms.IntegerField(widget=forms.HiddenInput())
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['groups'].queryset = user.groups.all()
    
class SRTLinkForm(forms.Form):
    srt_link = forms.URLField(
        label='RTSP Link',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'rtsp://your-url'})
    )