"""
Tests for user Auth
"""

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

import json
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

    def setUp(self):
        
        self.user = User.objects._create_user(
            nick_name = "admin",
            email = "admin@questioner.com",
            password = "@Admin123"
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