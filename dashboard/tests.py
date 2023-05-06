from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

from .models import *

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

class UserTestCase(APITestCase):

    """
    Test suite for User
    """
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "name": "Billy Smith",
            "agency": "Test Agency",
            "email": "billysmith@test.com"
        }
        self.url = "/user/"

    def test_create_user(self):
        '''
        test UserViewSet create method
        '''
        data = self.data
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().title, "Billy Smith")

    def test_create_user_without_name(self):
        '''
        test UserViewSet create method when name is not in data
        '''
        data = self.data
        data.pop("name")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_user_when_name_equals_blank(self):
        '''
        test UserViewSet create method when name is blank
        '''
        data = self.data
        data["name"] = ""
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_without_agency(self):
        '''
        test UserViewSet create method when agency is not in data
        '''
        data = self.data
        data.pop("agency")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_user_when_agency_equals_blank(self):
        '''
        test UserViewSet create method when agency is blank
        '''
        data = self.data
        data["agency"] = ""
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_without_email(self):
        '''
        test UserViewSet create method when email is not in data
        '''
        data = self.data
        data.pop("email")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_user_when_email_equals_blank(self):
        '''
        test UserViewSet create method when email is blank
        '''
        data = self.data
        data["email"] = ""
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_when_email_equals_non_email(self):
        '''
        test ContactViewSet create method when email is not email
        '''
        data = self.data
        data["email"] = "test"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)