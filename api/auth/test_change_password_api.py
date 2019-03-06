import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework.test import  APITestCase

from users.models import User


class ChangePassWordTest(APITestCase):

    def setUp(self):
        
        self.user = User.objects._create_user(
            nick_name = "dude",
            email = "dude@gmail.com",
            password = "dude@123456789"
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

    
    