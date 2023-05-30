from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status

from .models import *
from .viewsets import *

import logging
logger = logging.getLogger(__name__)

def create_stream(title, source, groups, created_by_id):
    """
    Create a livestream with the given `title`, `source`, `groups`, and `created_by_id`.
    Save it to the database and return the instance.
    """
    return Livestream.objects.create(title=title, source=source, groups=None, created_by_id=created_by_id)

def create_user(username, email, password, is_admin=False):
    """
    Create a user with the given `username`, `email`, `password`, and `is_admin`.
    Save it to the database and return the instance.
    """
    return CustomUser.objects.create(username=username, email=email, password=password, is_admin=is_admin)

def create_admin(username="testAdmin", email="testAdmin@admin.com", password="admin", is_admin=True):
    """
    Create an admin user with the given `username`, `email`, `password`, and `is_admin`.
    Save it to the database and return the instance.
    """
    return CustomUser.objects.create(username=username, email=email, password=password, is_admin=is_admin)

def init_groups():
    """
    Initialize groups in the database
    """
    Group.objects.create(name='Public')
    Group.objects.create(name='Private')
    Group.objects.create(name='Admin')

class CustomUserAPITests(APITestCase):

    """
    Test suite for CustomUser
    """
    def setUp(self):
        """
        Set self data to be used in tests
        """
        self.data = {
            "username": "testUser",
            "email": "testUser@test.com",
            "password": "testPassword",
            "is_admin": False,
            "viewports": []
        }

    def test_create_user(self):
        '''
        test UserViewSet create method
        '''
        user = create_user(self.data["username"], self.data["email"], self.data["password"], self.data["is_admin"])
        data = self.data

        newUser = CustomUser.objects.get(username=data["username"])
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(newUser.username, user.username)
        self.assertEqual(newUser.email, user.email)
        self.assertEqual(newUser.password, user.password)
        self.assertEqual(newUser.is_admin, user.is_admin)

    def test_user_permissions(self):
        '''
        test user permissions when accessing api
        '''
        user = create_user(self.data["username"], self.data["email"], self.data["password"], self.data["is_admin"])
        admin = create_admin()

        # test user permissions
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test admin permissions
        self.client.force_authenticate(user=admin)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class LivestreamAPITests(APITestCase):

    """
    Test suite for Livestream
    """
    def setUp(self):
        """
        Set self data to be used in tests
        """
        init_groups()
        self.admin = create_admin()
        self.data = {
            "title": "testStream",
            "source": "testSource",
            "created_by_id": self.admin.id
        }
        self.client.force_authenticate(user=self.admin)

    def test_create_public_livestream(self):
        response = self.client.post(reverse('livestream-list'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        newStream = Livestream.objects.get(title=self.data["title"])
        self.assertEqual(Livestream.objects.count(), 1)
        self.assertEqual(newStream.title, self.data["title"])
        self.assertEqual(newStream.source, self.data["source"])
        self.assertEqual(newStream.created_by_id, self.data["created_by_id"])
        self.assertEqual(newStream.created_by.username, self.admin.username)
        self.assertEqual(newStream.groups.count(), 1)
        self.assertEqual(newStream.groups.first().name, "Public")

    def test_create_private_livestream(self):
        self.data["groups"] = ["Private"]
        response = self.client.post(reverse('livestream-list'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        newStream = Livestream.objects.get(title=self.data["title"])
        self.assertEqual(Livestream.objects.count(), 1)
        self.assertEqual(newStream.title, self.data["title"])
        self.assertEqual(newStream.source, self.data["source"])
        self.assertEqual(newStream.created_by_id, self.data["created_by_id"])
        self.assertEqual(newStream.created_by.username, self.admin.username)
        self.assertEqual(newStream.groups.count(), 1)
        self.assertEqual(newStream.groups.first().name, "Private")

    def test_create_group_livestream(self):
        self.data["groups"] = ["Admin"]
        reponse = self.client.post(reverse('livestream-list'), self.data, format='json')
        self.assertEqual(reponse.status_code, status.HTTP_200_OK)

        newStream = Livestream.objects.get(title=self.data["title"])
        self.assertEqual(Livestream.objects.count(), 1)
        self.assertEqual(newStream.title, self.data["title"])
        self.assertEqual(newStream.source, self.data["source"])
        self.assertEqual(newStream.created_by_id, self.data["created_by_id"])
        self.assertEqual(newStream.created_by.username, self.admin.username)
        self.assertEqual(newStream.groups.count(), 1)
        self.assertEqual(newStream.groups.first().name, "Admin")


