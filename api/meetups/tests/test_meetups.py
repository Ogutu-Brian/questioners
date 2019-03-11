"""
Tests for meetup views and models
"""
from django.test import TestCase
from meetups.models import Meetup
from rest_framework.test import APIClient
from datetime import datetime
import django
import pytz
from users.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
import json
import os
from typing import Dict
from rest_framework.views import Response


class TestMeetupModel(TestCase):
    """
    Test for Meetup model
    """

    def setUp(self):
        """
        Setup for testing
        """
        self.user_data = self.get_test_data().get('user_data')
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
            scheduled_date=pytz.utc.localize(datetime.strptime(
                'Jun 2 2019 2:30PM', '%b %d %Y %I:%M%p')
            ))
        Meetup.objects.create(
            title='Cauchy Linear Homogenous Equations',
            body='A Math meetup to discuss Cauchy linear homogeneous equations',
            location='JKUAT',
            creator=self.admin,
            scheduled_date=pytz.utc.localize(datetime.strptime(
                'Dec 2 2019 2:30PM', '%b %d %Y %I:%M%p')
            ))

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

    def test_saving_into_database(self) -> None:
        """
        Tests that the data from models are being saved in the database
        """
        self.assertEqual(Meetup.objects.all().count(), 2)

    def test_duplicate_topic(self):
        """
        Tests duplication of topics in the database in same venue and same time
        """
        try:
            message = 'successfully created new meetup'
            Meetup.objects.create(
                title='Cauchy Linear Homogenous Equations',
                body='Time to meet the authors of logic',
                location='JKUAT',
                scheduled_date=pytz.utc.localize(datetime.strptime(
                    'Dec 2 2019 2:30PM', '%b %d %Y %I:%M%p')
                ))
        except django.db.utils.IntegrityError:
            message = 'Error occured during creation of meetup'
        finally:
            self.assertEqual(
                'Error occured during creation of meetup', message)

    def test_duplicate_meetup(self) -> None:
        """
        Tests creation of meetup with similar body to the same venue amd same time
        """
        try:
            message = 'successfully created new meetup'
            Meetup.objects.create(
                title='Mathematics Meetup',
                body='A Math meetup to discuss Cauchy linear homogeneous equations',
                location='JKUAT',
                scheduled_date=pytz.utc.localize(datetime.strptime(
                    'Dec 2 2019 2:30PM', '%b %d %Y %I:%M%p')
                ))
        except django.db.utils.IntegrityError:
            message = 'Error occured during creation of meetup'
        finally:
            self.assertEqual(
                'Error occured during creation of meetup', message)

    def test_persistence_of_data(self) -> None:
        """
        Tests for persistence of data iin the database
        """
        title = 'Cauchy Linear Homogenous Equations'
        scheduled_date = pytz.utc.localize(datetime.strptime(
            'Dec 2 2019 2:30PM', '%b %d %Y %I:%M%p')
        )
        meetup = Meetup.objects.filter(
            title=title, scheduled_date=scheduled_date)[0]
        self.assertEqual(meetup.scheduled_date, scheduled_date)
        self.assertEqual(
            meetup.body, 'A Math meetup to discuss Cauchy linear homogeneous equations')


class TestPostMeetup(TestMeetupModel):
    """
    Class for testing endpoints for meetups
    """

    def setUp(self):
        super().setUp()
        self.meetup_data = self.get_test_data().get('meetup_data')
        self.post_meetup_url = '/api/meetups'
        self.client = APIClient()

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
        self.client.force_authenticate(user=self.admin)

    def force_authenticate_user(self) -> None:
        """
        Force authenticates mormal user for testing
        """
        self.client.force_authenticate(user=self.user)

    def test_successfull_creation_of_meetup(self) -> None:
        """
        test successful creation of meetup
        """
        token, created = Token.objects.get_or_create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'),
                         self.meetup_data.get('title'))
        self.assertEqual(response.data.get('body'),
                         self.meetup_data.get('body'))
        self.assertEqual(response.data.get('location'),
                         self.meetup_data.get('location'))

    def test_unauthenticated_user(self) -> None:
        """
        Tests creation of meetup by unauthenticated user
        """
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('code'), 'not_authenticated')

    def test_posting_duplicate_meetups(self) -> None:
        """
        Tests creation of duplicate meetups
        """
        self.force_athenticate_admin()
        self.post_meetup()
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_non_admin_user(self) -> None:
        """
        Testa for the posting of meetups by users who are not administrators
        """
        self.client.credentials()
        self.force_authenticate_user()
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('error'),
                         'Admin only can create meetup')

    def test_missing_images(self) -> None:
        """
        Tests for successful creation of meetup without images
        """
        self.force_athenticate_admin()
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_tags(self) -> None:
        """
        Tests for successful creation of meetups without tags
        """
        self.force_athenticate_admin()
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_meetup_date(self) -> None:
        """
        Tests for posting of invalid date
        """
        self.force_athenticate_admin()
        self.meetup_data['scheduled_date'] = 'Invalid Date'
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_meetup_title(self) -> None:
        """
        Tests posting of meetups without a meetup title
        """
        self.force_athenticate_admin()
        self.meetup_data['title'] = ""
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_meetup_body(self) -> None:
        """
        Tests missing meetup body
        """
        self.force_athenticate_admin()
        self.meetup_data['body'] = ""
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_meetup_location(self) -> None:
        """
        Tests missing meetup location
        """
        self.force_athenticate_admin()
        self.meetup_data['location'] = ""
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_meetup_title(self) -> None:
        """
        Tests for invalid meetup titles
        """
        self.force_athenticate_admin()
        self.meetup_data['title'] = '?????//*&^£&%'
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get(
            'error'), '?????//*&^£&% is not a valid meetup title')

    def test_invalid_meetup_body(self) -> None:
        """
        Tests for an invalid meetup body
        """
        self.force_athenticate_admin()
        self.meetup_data['body'] = '#?-234+34```'
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get(
            'error'), '#?-234+34``` is not a valid meetup body')

    def test_invalid_meetup_location(self) -> None:
        """
        Tests for invalid meetup location input
        """
        self.force_athenticate_admin()
        self.meetup_data['location'] = '%23...*&^^^'
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get(
            'error'), '%23...*&^^^ is not a valid meetup location')

    def test_invalid_image_url(self) -> None:
        """
        Tests for an invalid image url for meetup
        """
        self.force_athenticate_admin()
        self.meetup_data['images'] = ['InvalidUrl']
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get(
            'error'), 'InvalidUrl is not a valid image url')


class TestViewMeetups(TestPostMeetup):
    """
    Tests for viewing meetups
    """

    def setUp(self):
        super().setUp()
        self.all_meetups_url = "/api/meetups"

    def create_meetup(self) -> None:
        """
        A method for creating meetups
        """
        self.force_athenticate_admin()
        self.post_meetup()

    def get_all_meetups(self) -> Response:
        """
        Tests that all meetups in the database can be retrieved
        """
        response = self.client.get(
            path=self.all_meetups_url,
            format='json'
        )
        return response

    def test_all_meetups_count(self):
        """
        Tests for the fetching of all meetups from the database
        """
        for i in range(4):
            self.create_meetup()
        self.assertEqual(4, len(self.get_all_meetups.data))
