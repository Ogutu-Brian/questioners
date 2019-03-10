import json
import responses
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase

from contextlib import contextmanager

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient, APITestCase

import os
from users.models import User

# Create your tests here.

User = get_user_model()
user_data = {
    'id': '001',
    'name': 'Abraham Kamau',
    'email': 'ericabraham806@gmail.com',
}


class BaseTest(APITestCase):
    """
    The base test class for all default test case settings
    """
    client = APIClient
    provider = 'google-oauth2'
    QUERY_STRINGS_RE = '\?([\w-]+(=[\w-]*)?(&[\w-]+(=[\w-]*)?)*)?$'

    base_url = 'https://www.googleapis.com/plus/v1/people/me'.replace(
        '.', r'\.')
    mock_url = re.compile(
        base_url + QUERY_STRINGS_RE
    )

    def login_user(self, email="", password=""):
        url = reverse("user_login")
        return self.client.post(
            url,
            data=json.dumps({
                "email": email,
                "password": password
            }),
            content_type="application/json"
        )

    def save_user(self):
        User.objects.create(
            name="Abraha Kamau",
            nick_name="greean",
            email="ericabraham806@gmail.com",
            password="@Us3r.com"
        )

    

    def setUp(self):

        self.user = User.objects._create_user(
            nick_name="admin",
            email="admin@questioner.com",
            password="@Admin123"
        )
        self.social_url = reverse("social")

        self.token = os.getenv('GoogleAccessToken')
        self.bad_token = 'badtokendhbi'
        self.provider = 'google-oauth2'
        self.invalid_provider = 'google'
        self.no_provider = ''

    def social_login(self, provider, token):
        social_url = reverse("social")
        return self.client.post(
            social_url,
            data=json.dumps({
                "access_token": token,
                "provider": provider
            }),
            content_type="application/json"
        )

class LoginTest(BaseTest):
    """
    Tests for auth/login endpoint
    """

    def test_login_correct_credentials(self):
        """
        Test correct user login credentials
        """
        response = self.login_user("admin@questioner.com", "@Admin123")
        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_login_incorrect_credentials(self):
        """
        Test incorrect user login credentials
        """
        response = self.login_user("abraham", "aBu#123")
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)


class GoogleOAuthTest(BaseTest):
    """
    Tests for google authentication using OAuth2
    """
    def test_successful_google_login(self):
        response = self.social_login(self.provider, self.token)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_unsuccessful_google_login(self):
        response = self.social_login(self.provider, self.bad_token)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_no_provider(self):
        response = self.social_login(self.no_provider,self.token)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_invalid_provider(self):
        response = self.social_login(self.invalid_provider, self.token)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
    
   