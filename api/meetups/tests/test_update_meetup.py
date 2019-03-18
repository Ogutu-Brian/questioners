from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from users.models import User
from meetups.models import Meetup
from django.utils import timezone


class BaseTest(APITestCase):
    """
    The base test class for all default test case settings
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects._create_user(
            name="Issa Mwangi",
            email="issaianmaina@gmail.com",
            password="@12345gh"
        )
        self.user.is_active = True
        self.user.save()
        self.admin = User.objects._create_user(
            name="Issa Mwangi",
            email="issamwangi@gmail.com",
            password="@Admin123"
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
            title='Test Driven',
            body='Developers need to discusss the correct approach of doing',
            location='Andela Campus',
            creator=self.admin,
            scheduled_date=timezone.now()+timezone.timedelta(days=2)
        )

        self.meetup = Meetup.objects.all()[0]
        self.id = str(self.meetup.id)

        self.update_data = {
            'title': 'My new title',
            'body': 'New awesome body'
        }
        self.invalid_title = {
            'title': '!@#$%^&*'
        }
        self.duplicated_title = {
            'title': 'Test Driven Development'
        }
        self.invalid_location = {
            'location': '@#$%^&*'
        }
        self.update_meetup_url = '/api/meetups/'
        self.unexisting_meetup_url = '/api/meetups/233dtui666798htr567/'

    def test_admin_successful_update(self):
        token, created = Token.objects.get_or_create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        response = self.client.put(
            path=self.update_meetup_url+self.id+'/',
            data=self.update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_normal_user_unsuccessful_update(self):
        token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        response = self.client.put(
            path=self.update_meetup_url+self.id+'/',
            data=self.update_data,
            format='json'
        )
        self.assertEqual(response.data['Error'],
                         'Only an admin user can update a meetup')

    def test_update_a_non_existence_meetup(self):
        token, created = Token.objects.get_or_create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        response = self.client.put(
            path=self.unexisting_meetup_url,
            data=self.update_data,
            format='json'
        )
        self.assertEqual(response.data[0]['Error'],
                         'The specified meetup does not exist')

    def test_invalid_title_update(self):
        token, created = Token.objects.get_or_create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        response = self.client.put(
            path=self.update_meetup_url+self.id+'/',
            data=self.invalid_title,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]['error'],
                         '!@#$%^&* is not a valid meetup title')

    def test_invalid_location_update(self):
        token, created = Token.objects.get_or_create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        response = self.client.put(
            path=self.update_meetup_url+self.id+'/',
            data=self.invalid_location,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]['error'],
                         '@#$%^&* is not a valid meetup location')

    def test_updating_same_existing_title(self):
        token, created = Token.objects.get_or_create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        response = self.client.put(
            path=self.update_meetup_url+self.id+'/',
            data=self.duplicated_title,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
