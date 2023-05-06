from django.contrib.gis import admin
from .models import *

admin.site.register(MapChoice)
admin.site.register(Marker)
admin.site.register(Agency)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "agency","email")