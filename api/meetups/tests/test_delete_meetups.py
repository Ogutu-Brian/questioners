import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.utils import timezone
from datetime import datetime

from users.models import User
from meetups.models import Meetup

URL_LOGIN = api_reverse("user_login")


class DeleteMeetTest(APITestCase):

    '''
    Test for Delete meetup endpoint
    '''

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects._create_user(
            nick_name="dude",
            email="dude@gmail.com",
            password="mycurrentpassword"
        )
        self.user.is_active = True
        self.user.is_admin = True
        self.user.save()
        self.delete_url = '/api/meetups/'
        self.data_login = {
            "email": "dude@gmail.com",
            "password": "mycurrentpassword"
        }
        self.meetup = Meetup.objects.create(
            title='This is a test title',
            body='This is a Test Boby',
            location='This is a Test location',
            creator=self.user,
            scheduled_date=timezone.now() + timezone.timedelta(days=3)
        )
        self.meetup.save()
        self.meetup_id = str(Meetup.objects.all()[0].id)
        self.invalid_meetup_id = 'sjjhsjshh8899whuh'

    def is_authenticated(self):
        '''
        Authenticate user
        '''
        response = self.client.post(URL_LOGIN, self.data_login, format='json')
        token = response.data.get("token", None)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_delete_correct_meetid(self):
        '''
        test to delete the correct meetup id
        '''
        self.is_authenticated()
        response = self.client.delete(path=self.delete_url+self.meetup_id+'/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_meetid_notfound(self):
        '''
        test for delete meetup id notfound
        '''
        self.is_authenticated()
        [meetup.delete() for meetup in Meetup.objects.all()]
        response = self.client.delete(path=self.delete_url+self.meetup_id+'/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_invalid_meetupid(self):
        '''
        test for delete invalid meetup id
        '''
        self.is_authenticated()
        response = self.client.delete(
            path=self.delete_url+self.invalid_meetup_id+'/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_is_authenticated(self):
        '''
        test if user is_authenticated
        '''

        response = self.client.delete(path=self.delete_url+self.meetup_id+'/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
