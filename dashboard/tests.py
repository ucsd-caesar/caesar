from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status

from unittest.mock import patch

from .models import *
from .viewsets import *

import requests
import json
import subprocess
import logging
logger = logging.getLogger(__name__)

ADMIN_USER = "testAdmin"
ADMIN_EMAIL = "testAdmin@admin.com"
ADMIN_PASS = "admin"
TIMEOUT = 2

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

def create_admin(username=ADMIN_USER, email=ADMIN_EMAIL, password=ADMIN_PASS, is_admin=True):
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
    @classmethod
    def setUpTestData(self):
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
    @classmethod
    def setUpTestData(self):
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

    def test_create_public_livestream(self):
        self.client.force_authenticate(user=self.admin)
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
        self.client.force_authenticate(user=self.admin)
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
        self.client.force_authenticate(user=self.admin)
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

    def test_create_multiple_types_livestream(self):
        self.client.force_authenticate(user=self.admin)
        self.data["source"] = "rtsp://testSource"
        response = self.client.post(reverse('livestream-list'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        newStream = Livestream.objects.get(id=response.data["id"])
        self.assertEqual(Livestream.objects.count(), 1)
        self.assertEqual(newStream.type, "rtsp")

        self.data["source"] = "rtmp://testSource"
        response = self.client.post(reverse('livestream-list'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        newStream = Livestream.objects.get(id=response.data["id"])
        self.assertEqual(Livestream.objects.count(), 2)
        self.assertEqual(newStream.type, "rtmp")

        self.data["source"] = "hls://testSource"
        response = self.client.post(reverse('livestream-list'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        newStream = Livestream.objects.get(id=response.data["id"])
        self.assertEqual(Livestream.objects.count(), 3)
        self.assertEqual(newStream.type, "hls")

        self.data["source"] = "webrtc://testSource"
        response = self.client.post(reverse('livestream-list'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        newStream = Livestream.objects.get(id=response.data["id"])
        self.assertEqual(Livestream.objects.count(), 4)
        self.assertEqual(newStream.type, "webrtc")

        self.data["source"] = "http://testSource"
        response = self.client.post(reverse('livestream-list'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        newStream = Livestream.objects.get(id=response.data["id"])
        self.assertEqual(Livestream.objects.count(), 5)
        self.assertEqual(newStream.type, "http")

        self.data["source"] = "somethingelse://testSource"
        response = self.client.post(reverse('livestream-list'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        newStream = Livestream.objects.get(id=response.data["id"])
        self.assertEqual(Livestream.objects.count(), 6)
        self.assertEqual(newStream.type, "other")

class StreamAuthenticationTests(TestCase):
    """
    Test suite for Livestream authentication
    """
    @classmethod
    def setUpTestData(self):
        """
        Set self data to be used in tests
        """
        init_groups()
        self.admin = create_admin()

        data = {
            "username": "testUser",
            "email": "testUser@test.com",
            "password": "testPassword",
            "is_admin": False,
            "viewports": []
        }

        self.user = create_user(data["username"], data["email"], data["password"], data["is_admin"])

        # create path configuration for ADMIN_USER
        with open('dev/json/path.json') as f:
            r = requests.post("http://mediamtx:9997/v2/config/paths/add/" + str(self.admin.id), json=json.load(f))

        print("Path configuration created for ADMIN_USER with id: " + str(self.admin.id))
        
        # url to return path configuration for ADMIN_USER
        self.path_url = "http://mediamtx:9997/v2/paths/get/" + str(self.admin.id)

        # start celery worker
        with patch('subprocess.run') as mock:
            mock.return_value = None
            subprocess.run(["celery", "multi", "restart", "1", "-A", "config", "-l", "INFO", "-P", "eventlet", "-c", "1000"])
            mock.assert_called_once_with(["celery", "multi", "restart", "1", "-A", "config", "-l", "INFO", "-P", "eventlet", "-c", "1000"])

    def test_create_livestream_no_auth(self):
        """
        Test that a user cannot create a livestream without authentication
        """
        r = requests.get(self.path_url)
        try:
            r.json() # if json is returned, then the path exists
        except requests.exceptions.JSONDecodeError:
            raise Exception("Path does not exist")

        rtsp_url = "rtsp://mediamtx:8554/" + str(self.admin.id)
        output = subprocess.run(["ffmpeg", "-re", "-stream_loop", "-1", "-i", "dev/media/Rices.ts", "-c:v", "copy", "-c:a", "aac", "-bsf:a", "aac_adtstoasc", "-f", "rtsp", "-rtsp_transport", "tcp", rtsp_url])
        self.assertEqual(output.returncode, 1) # ffmpeg should fail to connect

    def test_create_livestream_wrong_pass(self):
        """
        Test that a user cannot create a livestream with wrong password
        """
        r = requests.get(self.path_url)
        try:
            r.json() # if json is returned, then the path exists
        except requests.exceptions.JSONDecodeError:
            raise Exception("Path does not exist")

        rtsp_url = "rtsp://" + ADMIN_USER + ":wrongpass@mediamtx:8554/" + str(self.admin.id)
        output = subprocess.Popen(["ffmpeg", "-re", "-stream_loop", "-1", "-i", "dev/media/Rices.ts", "-c:v", "copy", "-c:a", "aac", "-bsf:a", "aac_adtstoasc", "-f", "rtsp", "-rtsp_transport", "tcp", rtsp_url])
        try:
            # subprocess should timeout
            output.communicate(timeout=TIMEOUT)
            self.assertEqual(output.returncode, 1)
        except subprocess.TimeoutExpired:
            output.terminate()  
    
    def test_create_livestream_no_path(self):
        """
        Test that a user cannot create a livestream at a path that does not exist
        """
        non_path_url = "http://mediamtx:9997/v2/paths/get/nonPath"
        r = requests.get(non_path_url)
        try:
            r.json() # if json is returned, then the path exists
            raise Exception("Path exists")
        except requests.exceptions.JSONDecodeError:
            self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND) # the path should not exist

        rtsp_url = "rtsp://" + ADMIN_USER +":"+ ADMIN_PASS + "@mediamtx:8554/nonPath"
        output = subprocess.run(["ffmpeg", "-re", "-stream_loop", "-1", "-i", "dev/media/Rices.ts", "-c:v", "copy", "-c:a", "aac", "-bsf:a", "aac_adtstoasc", "-f", "rtsp", "-rtsp_transport", "tcp", rtsp_url])
        self.assertEqual(output.returncode, 1) # ffmpeg should fail to connect

    def test_create_livestream_wrong_path(self):
        """
        Test that a user cannot create a livestream at a path that is not theirs
        """
        r = requests.get(self.path_url)
        try:
            r.json() # if json is returned, then the path exists
        except requests.exceptions.JSONDecodeError:
            raise Exception("Path does not exist")

        rtsp_url = "rtsp://" + ADMIN_USER +":"+ ADMIN_PASS + "@mediamtx:8554/" + str(self.admin.id + 1)
        output = subprocess.Popen(["ffmpeg", "-re", "-stream_loop", "-1", "-i", "dev/media/Rices.ts", "-c:v", "copy", "-c:a", "aac", "-bsf:a", "aac_adtstoasc", "-f", "rtsp", "-rtsp_transport", "tcp", rtsp_url])
        try:
            # subprocess should timeout
            output.communicate(timeout=TIMEOUT)
            self.assertEqual(output.returncode, 1)
        except subprocess.TimeoutExpired:
            output.terminate()  

    def test_create_livestream_correct(self):
        """
        Test that a user can create a livestream at an authorized path with correct password
        """
        r = requests.get(self.path_url)
        try:
            r.json() # if json is returned, then the path exists
            print(r.json())
        except requests.exceptions.JSONDecodeError:
            raise Exception("Path does not exist")
        
        rtsp_url = "rtsp://" + ADMIN_USER +":"+ ADMIN_PASS + "@mediamtx:8554/" + str(self.admin.id)
        print("RTSP URL: " + rtsp_url)
        output = subprocess.Popen(["ffmpeg", "-re", "-stream_loop", "-1", "-i", "dev/media/Rices.ts", "-c:v", "copy", "-c:a", "aac", "-bsf:a", "aac_adtstoasc", "-f", "rtsp", "-rtsp_transport", "tcp", rtsp_url])
        try:
            output.communicate(timeout=TIMEOUT)
            print(output)
            self.assertEqual(output.returncode, 0) # subprocess should not timeout
        except subprocess.TimeoutExpired:
            output.terminate()
            raise Exception("Livestream did not start")

