import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient, APITestCase

from users.models import User

# Create your tests here.


class UserTestCase(TestCase):
    """Dummy test case for user"""

    def test_user_was_saved(self):
        """Dummy"""
        user = User.objects.create(name="Brian", nick_name="Ogutu",
                                   email="codingbrian58@gmail.com",
                                   password="Henkdebruin58")
        self.assertEqual(user.name, "Brian")
        self.assertEqual(user.email, "codingbrian58@gmail.com")


class YourTestClass(TestCase):

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
"""
Tests for user Auth
"""



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
        self.assertIn("auth_token", response.data)
        self.assertEqual(response.status_code, HTTP_200_OK)
    
    def test_login_incorrect_credentials(self):
        """
        Test incorrect user login credentials
        """
        response = self.login_user("abraham", "aBu#123")
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
