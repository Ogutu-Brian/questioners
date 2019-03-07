from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework.test import  APITestCase

from .models import User

class TestEmailSent(APITestCase):
    """
    test for class to send password reset link to email
    """
    def setUp(self):
        """
        set up method to test email to be sent endpoint
        """
        self.url = api_reverse('reset_password')
        self.register_url = api_reverse('user_signup')
        self.user =  {
            'user' : {
                'username': 'philip',
                'email': 'philino92@gmail.com',
                'password': 'philip2345'
            }
        }
        self.client.post(self.register_url, self.user, format="json")
        User.is_active = True

    def test_unregistered_email(self):
        """
        case where unregistered user tries to request a password
        """
        response = self.client.post(self.url, data={"email":"philipsiko@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)