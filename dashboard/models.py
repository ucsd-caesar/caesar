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

class Agency(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class User(models.Model):
    name = models.CharField(max_length=255)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.name