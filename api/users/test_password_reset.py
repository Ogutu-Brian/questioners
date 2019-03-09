from rest_framework.test import  APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
import json
from .models import User


class TestPasswordReset(APITestCase):
    """
    test for class to resetnpassword using mail
    """

    def setUp(self):
        """
        set up method to test email to be sent endpoint
        """
        self.client = APIClient()
        self.url = api_reverse('user_signup')
        self.email_url = api_reverse('reset_password')
        self.reset_url = api_reverse('reset_password_confirm')

        self.user_data = {
            "name": "philp",
            "nick_name": 'ototo',
            "email": 'test@gmail.com',
            "password": 'adminPaswiseadmsw0rd'
        }
        
    def user_sigup_details(self):
        """
        This method signs up a user and returns
        user id and the token
        """
        data = self.user_data
        self.response = self.client.post(self.url, data, format="json")
        user_id, token = self.response.context['uid'], self.response.context['token']
        return user_id, token

    def test_email_field_missing(self):
        """
        case where a user provides no parameters on request body
        """
        response = self.client.post(self.email_url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"email":["This field is required."]}')

    def test_unregistered_email(self):
        """
        case where unregistered user tries to request a password
        """
        response = self.client.post(self.email_url, data={"email":"philipsiko@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content, b'{"detail":"User account with given email does not exist.","code":"not_found"}')
        
    def test_empty_email(self):
        """
        case where user tries to request a password reset with empty email
        """
        response = self.client.post(self.email_url, data={"email":""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"email":["This field may not be blank."]}')
        
    def test_reset_password(self):
        """
        tests for reset password
        """

        data = self.user_sigup_details()
        self.activation_data = {
            "uid": data[0],
            "token": data[1]
        }

        #reset confirm password
        self.reset_confirm_data = {
            "uid": self.activation_data['uid'],
            "token": self.activation_data['token'],
            "new_password": "mynewpassword",
            "re_new_password": "mynewpassword"
        }

        self.response = self.client.post(self.reset_url,
            self.reset_confirm_data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.response.content, b'{"message":"password successfully reset"}')
        
        
    def test_reset_with_unactivated_account(self):
        """
        Test method to ensure users cannot reset password with unverified
        email address when signing in
        """
        # sign-up user
        data = self.user_data

        self.client.post(self.url, data, format="json")
        #reset password before verifying email address
        self.response = self.client.post(
            self.email_url,
            self.user_data['email'],
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)



