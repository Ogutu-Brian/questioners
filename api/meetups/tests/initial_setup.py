"""
Contains shared methods and properties
"""
from django.test import TestCase
from meetups.models import Meetup
from rest_framework.test import APIClient
from users.models import User
import json
import os
from typing import Dict
from rest_framework.views import Response
from django.utils import timezone
from rest_framework.authtoken.models import Token



class TestSetUp(TestCase):
    """
    Test for Meetup model
    """

    def setUp(self):
        """
        Setup for testing
        """
        self.user_data = self.get_test_data().get('user_data')
        self.meetup_data = self.get_test_data().get('meetup_data')
        self.post_meetup_url = '/api/meetups'
        self.all_meetups_url = '/api/meetups/'
        self.upcoming_meetups_url = '/api/meetups/upcoming/'
        self.client = APIClient()
        user = self.user_data.get('user')
        admin = self.user_data.get('admin')
        self.user = User.objects.create(
            email=user.get('email'),
            name=user.get('name'),
            nick_name=user.get('nick_name'),
            password=user.get('password')
        )
        self.user.is_active = True
        self.user.save()
        self.admin = User.objects.create(
            email=admin.get('email'),
            name=admin.get('name'),
            nick_name=admin.get('nick_name'),
            password=admin.get('password')
        )
        self.admin.is_active = True
        self.admin.is_staff = True
        self.admin.save()
        Meetup.objects.create(
            title='Test Driven Development',
            body='Developers need to discusss the correct approach of doing test driven development',
            location='Andela Campus',
            creator=self.admin,
            scheduled_date=timezone.now()+timezone.timedelta(days=3)
        )
        Meetup.objects.create(
            title='Cauchy Linear Homogenous Equations',
            body='A Math meetup to discuss Cauchy linear homogeneous equations',
            location='JKUAT',
            creator=self.admin,
            scheduled_date=timezone.now()+timezone.timedelta(days=3)
        )

    def get_test_data(self) -> Dict:
        """
        Reads test data from test_data.json file
        """
        __location__ = os.path.realpath(
            os.path.join(
                os.getcwd(),
                os.path.dirname(__file__)
            )
        )
        with open(os.path.join(__location__, 'test_data.json')) as record:
            data = json.load(record)
        return data

    def post_meetup(self) -> Response:
        """
        Method for posting meetups during testing
        """
        response = self.client.post(
            path=self.post_meetup_url,
            data=self.meetup_data,
            format='json'
        )
        return response

    def force_athenticate_admin(self) -> None:
        """
        Force authenticates an admin user for testing
        """
        token, created = Token.objects.get_or_create(user=self.admin)
        return self.client.credentials(HTTP_AUTHORIZATION="token " + token.key)
    def force_authenticate_user(self) -> None:
        """
        Force authenticates mormal user for testing
        """
        token, created = Token.objects.get_or_create(user=self.user)
        return self.client.credentials(HTTP_AUTHORIZATION="token " + token.key)

    def clear_meetups(self) -> None:
        """
        clears all meetup data from the database
        """
        [meetup.delete() for meetup in Meetup.objects.all()]

    def create_meetup(self) -> Response:
        """
        A method for creating meetups
        """
        self.force_athenticate_admin()
        response = self.post_meetup()
        return response

    def get_specific_meetup(self, meetup_id: str) -> Response:
        """
        Gets a specific meetup given a meetup id
        """
        response = self.client.get(path=self.all_meetups_url+meetup_id)
        return response

    def get_upcoming_meetups(self) -> Response:
        """
        Gets upcoming meetups
        """
        response = self.client.get(path=self.upcoming_meetups_url)
        return response

    def get_all_meetups(self) -> Response:
        """
        Tests that all meetups in the database can be retrieved
        """
        response = self.client.get(
            path=self.all_meetups_url,
            format='json'
        )
        return response
