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
