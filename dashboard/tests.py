from django.test import TestCase
from django.urls import reverse

from .models import Marker

def create_marker(name, location):
    """
    Create a marker with the given `name` and `location`.
    """
    return Marker.objects.create(name=name, location=location)

class MarkerTests(TestCase):

    def test_addMarker(self):
        """
        ensure that a marker can be added correctly 
        """
        marker = create_marker("testMarker", "POINT (0 0)")
        response = self.client.get(reverse('api/markers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, marker.name)
        self.assertContains(response, marker.location)

