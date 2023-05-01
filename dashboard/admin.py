from django.contrib.gis import admin
from .models import *
import pandas as pd

admin.site.register(MapChoice)
admin.site.register(Marker)

class CameraAdmin(admin.ModelAdmin):
    fields = ['name', 'source', 'location']
    list_display = ('name', 'source', 'location')

    data = pd.read_csv('dashboard/hpwrencodes.csv')
    codes = data['code']
    names = data['name']
    directions = {'n':'North','e':'East','s':'South','w':'West'}
    added = False

    for i in range(0,codes.size):
        source = 'https://hpwren.ucsd.edu/cameras/L/'+codes[i]+'-'+'n'+'-mobo-c'+'.jpg'
        Camera.objects.create(name=names[i], source=source)

admin.site.register(Camera, CameraAdmin)
