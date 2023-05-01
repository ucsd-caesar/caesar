from django.contrib.gis.db import models

class MapChoice(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Marker(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField()

    def __str__(self):
        return self.name
    
class Camera(models.Model):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    location = models.PointField(default='POINT(0.0 0.0)')

    def __str__(self):
        return self.name
    