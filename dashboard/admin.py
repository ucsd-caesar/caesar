from django.contrib.gis import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MapChoice, Marker, Agency, Livestream, CustomUser, Viewport
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(MapChoice)
admin.site.register(Marker)
admin.site.register(Agency)
admin.site.register(Livestream)

class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

    def clean_password2(self):
        # check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and (password1 != password2):
            raise forms.ValidationError("Passwords do not match")
        return password2
    
    def save(self, commit=True):
        # save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ViewportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_created', 'time_created')
    readonly_fields = ('date_created', 'time_created', 'livestreams')

admin.site.register(Viewport, ViewportAdmin)

class CustomUserChangeForm(UserChangeForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'is_active', 'is_admin')

class UserAdmin(BaseUserAdmin):
    # the forms to add and change user instances
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # the fields to be used in displaying the User model
    # these override the definitions on the base UserAdmin
    # that reference specific fields on auth.User
    list_display = ('username', 'id', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    readonly_fields = ('created_livestreams', 'viewports')
    # add_fieldsets is not a standard ModelAdmin attribute
    # UserAdmin overrides get_fieldsets to use this attribute when creating a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
            ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin
admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
