import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User

URL_LOGIN = api_reverse("user_login")
URL_CHANGE_PASSWORD = api_reverse('change_password')


class ChangePassWordTest(APITestCase):

    client = APIClient

    def setUp(self):

        self.user = User.objects._create_user(
            nick_name="dude",
            email="dude@gmail.com",
            password="mycurrentpassword"
        )
        self.data_correct_fields = {
            "new_password": "newpassword@dude",
            "re_new_password": "newpassword@dude",
            "current_password": "mycurrentpassword"
        }
        self.data_login = {
            "email": "dude@gmail.com",
            "password": "mycurrentpassword"
        }
        self.data_blank_fields = {
            "new_password": "",
            "re_new_password": "",
            "current_password": ""
        }
        self.data_wrong_retype_password = {
            "new_password": "newpassword@dude",
            "re_new_password": "NNewpassword@dude",
            "current_password": "mycurrentpassword"
        }
        self.data_wrong_current_password = {
            "new_password": "newpassword@dude",
            "re_new_password": "newpassword@dude",
            "current_password": "notmycurrentpassword"
        }
        response = self.client.post(URL_LOGIN, self.data_login, format='json')
        token = response.data.get("auth_token", None)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_incorrect_current_password(self):
        '''
        test for change password with incorrect current password

        '''
        response = self.client.post(
            URL_CHANGE_PASSWORD, self.data_wrong_current_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_authorized_user(self):
        '''
        test for a logged in user change password

        '''

        response = self.client.post(
            URL_CHANGE_PASSWORD, self.data_correct_fields, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_change_password_blank_fields(self):
        '''
        test for change password with blank fields

        '''
        response = self.client.post(
            URL_CHANGE_PASSWORD, self.data_blank_fields, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_with_incorrecct_retype_password(self):
        '''
        test for change password with incorrect Retype_password

        '''

        response = self.client.post(
            URL_CHANGE_PASSWORD, self.data_wrong_retype_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
