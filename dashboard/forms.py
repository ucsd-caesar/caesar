from django import forms
from django.contrib.auth.models import Group
from django.db.models import Q
from .models import CustomUser, Livestream

class InviteUserForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email does not exist.")
        return email

class LivestreamVisibilityForm(forms.ModelForm):
    form_name = forms.CharField(widget=forms.HiddenInput(), initial='visibility_form')
    livestream_id = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Livestream
        fields = ('groups', 'livestream_id')

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(), 
        widget=forms.CheckboxSelectMultiple,
        required=False)
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # add all groups that the user is a member of and the Public/Private groups to queryset
        self.fields['groups'].queryset = Group.objects.filter(Q(id__in=user.groups.all()) | Q(name__in=['Public', 'Private']))

class SRTLinkForm(forms.Form):
    srt_link = forms.URLField(
        label='RTSP Link',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'rtsp://your-url'})
    )