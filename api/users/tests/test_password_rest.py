from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
import json
from users.models import User

class TestEmailSent(APITestCase):
    """
    test for class to send password reset link to email
    """
    def setUp(self):
        """
        set up method to test email to be sent endpoint
        """
        self.url = api_reverse('reset_password')
        self.user = User.objects.create(
                name = 'kevin',
                email = 'philipkevin92@gmail.com',
                password = 'Kevin12345'
        )

    def test_email_field_missing(self):
        """
        case where a user provides no parameters on request body
        """
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"email":["This field is required."]}')

    def test_unregistered_email(self):
        """
        case where unregistered user tries to request a password
        """
        response = self.client.post(self.url, data={"email":"philipsiko@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content, b'{"detail":"User account with given email does not exist.","code":"not_found"}')
        
    def test_empty_email(self):
        """
        case where user tries to request a password reset with empty email
        """
        response = self.client.post(self.url, data={"email":""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"email":["This field may not be blank."]}')
        
    def test_successful_email_sent(self):
        """
        case where a user provides valid credentials
        """
        response = self.client.post(self.url, data={"email":"philipkevin92@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"message":"reset link sent to your mail"}')

            
class TestPasswordReset(APITestCase):
    """
    test for class to reset password using mail
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
        
    def user_details(self):
        """
        This method signs up a user and returns
        user id and the token
        """
        data = self.user_data
        self.response = self.client.post(self.url, data, format="json")
        user_id, token = self.response.context['uid'], self.response.context['token']
        return user_id, token


    def test_reset_password(self):
        """
        tests for reset password
        """

        data = self.user_details()
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
        