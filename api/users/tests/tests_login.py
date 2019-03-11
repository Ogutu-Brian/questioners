import json
import responses
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase

from contextlib import contextmanager

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

import os
from users.models import User

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

        self.user1 = User.objects._create_user(
            name="Issa Mwangi",
            email="issamwangi@gmail.com",
            password="@Admin123"
        )
        self.user2 = User.objects._create_user(
            name="Abraham Kamau",
            email="admin@questioner.com",
            password="@Admin123"
        )
        self.social_url = reverse("social")

        self.token = os.getenv('GoogleIdToken')
        self.token2 = os.getenv('GoogleIdTokenNouser')
        self.bad_token = 'badtokendhibhbcububi'

    def social_login(self, token):
        social_url = reverse("social")
        return self.client.post(
            social_url,
            data=json.dumps({
                "id_token": token
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_incorrect_credentials(self):
        """
        Test incorrect user login credentials
        """
        response = self.login_user("abraham", "aBu#123")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class GoogleLoginTest(BaseTest):
#     """
#     Tests for user login with Google OAuth2
#     """

#     def test_successful_google_login(self):
#         """
#         Test correct id_token with existing user
#         """
#         response = self.social_login(self.token)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_bad_token_google_login(self):
#         """
#         Tests bad token
#         """
#         response = self.social_login(self.bad_token)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_no_user_found_google_login(self):
#         """
#         Tests no user in the database
#         """
#         response = self.social_login(self.token2)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
