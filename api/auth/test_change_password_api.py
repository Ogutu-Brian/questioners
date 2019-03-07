import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework.test import  APITestCase, APIClient

from users.models import User


class ChangePassWordTest(APITestCase):

    client = APIClient

    def setUp(self):
        
        self.user = User.objects._create_user(
            nick_name = "dude",
            email = "dude@gmail.com",
            password = "mycurrentpassword"
        )

    def test_change_password_unauthorized(self):
        '''
        only logged in users can change password

        '''
        url = api_reverse('change_password')
        data = {
            "new_password": "newpassword@dude",
            "re_new_password": "newpassword@dude",
             "current_password": "mycurrentpassword"
        }
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password_authorized_user(self):
        '''
        test for a logged in user change password

        '''
        url_login = api_reverse("user_login")
        data_login={
            "email":"dude@gmail.com",
            "password":"mycurrentpassword"
        }

        url = api_reverse('change_password')
        data = {
            "new_password": "newpassword@dude",
            "re_new_password": "newpassword@dude",
             "current_password": "mycurrentpassword"
        }
        response = self.client.post(url_login,data_login, format='json')
        token = response.data.get("auth_token",None)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2 = self.client.post(url,data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_204_NO_CONTENT)


    def test_change_password_blank_fields(self):
        '''
        test for change password with blank fields

        '''
        url_login = api_reverse("user_login")
        data_login={
            "email":"dude@gmail.com",
            "password":"mycurrentpassword"
        }

        url = api_reverse('change_password')
        data = {
            "new_password": "",
            "re_new_password": "",
             "current_password": ""
        }
        response = self.client.post(url_login,data_login, format='json')
        token = response.data.get("auth_token",None)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2 = self.client.post(url,data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_change_password_with_incorrecct_Retype_password(self):
        '''
        test for change password with incorrect Retype_password

        '''
        url_login = api_reverse("user_login")
        data_login={
            "email":"dude@gmail.com",
            "password":"mycurrentpassword"
        }

        url = api_reverse('change_password')
        data = {
            "new_password": "newpassword@dude",
            "re_new_password": "NNewpassword@dude",
            "current_password": "mycurrentpassword"
        }
        response = self.client.post(url_login,data_login, format='json')
        token = response.data.get("auth_token",None)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2 = self.client.post(url,data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)