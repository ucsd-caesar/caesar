from django.contrib.gis.db import models
from django.contrib.auth.models import User

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
    
class Livestream(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_livestreams')

    def __str__(self):
        return self.title

class Agency(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='memberships')

    @property
    def getLivestreams(self):
        # Returns all active livestreams from all of its members
        return Livestream.objects.filter(created_by__in=self.members.all())

    def __str__(self):
        return self.name
    
class User(models.Model):
    name = models.CharField(max_length=255)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.name