"""
Tests for meetup views and models
"""
from meetups.tests.initial_setup import TestSetUp
from rest_framework import status
import django
from meetups.models import Meetup, Rsvp
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.test import TestCase
from rest_framework.test import APIClient
import json
from users.models import User
from rest_framework.reverse import reverse
from rest_framework.response import Response


class TestMeetupModel(TestSetUp):
    """
    Test for Meetup model
    """

    def setUp(self):
        super().setUp()

    def test_saving_into_database(self) -> None:
        """
        Tests that the data from models are being saved in the database
        """
        self.assertEqual(Meetup.objects.all().count(), 2)

    def test_integrity(self):
        """
        Tests if a meetup can be created by uknownimous user
        """
        try:
            message = 'successfully created new meetup'
            Meetup.objects.create(
                title='Math Meetup',
                body='Time to meet the authors of logic',
                location='JKUAT',
                scheduled_date=timezone.now()+timezone.timedelta(days=3)
            )
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
        meetup = Meetup.objects.filter(title=title)[0]
        self.assertEqual(
            meetup.body, 'A Math meetup to discuss Cauchy linear homogeneous equations')


class TestPostMeetup(TestSetUp):
    """
    Class for testing endpoints for meetups
    """

    def setUp(self):
        super().setUp()

    def test_successfull_creation_of_meetup(self) -> None:
        """
        test successful creation of meetup
        """
        token, created = Token.objects.get_or_create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        response = self.post_meetup()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('data').get('title'),
                         self.meetup_data.get('title'))
        self.assertEqual(response.data.get('data').get('body'),
                         self.meetup_data.get('body'))
        self.assertEqual(response.data.get('data').get('location'),
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
        self.create_meetup()
        response = self.create_meetup()
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
        response = self.create_meetup()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_tags(self) -> None:
        """
        Tests for successful creation of meetups without tags
        """
        response = self.create_meetup()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_meetup_date(self) -> None:
        """
        Tests for posting of invalid date
        """
        self.meetup_data['scheduled_date'] = 'Invalid Date'
        response = self.create_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_meetup_title(self) -> None:
        """
        Tests posting of meetups without a meetup title
        """
        self.meetup_data['title'] = ""
        response = self.create_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_meetup_body(self) -> None:
        """
        Tests missing meetup body
        """
        self.meetup_data['body'] = ""
        response = self.create_meetup()
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
        self.meetup_data['title'] = '?????//*&^£&%'
        response = self.create_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get(
            'error'), '?????//*&^£&% is not a valid meetup title')

    def test_invalid_meetup_body(self) -> None:
        """
        Tests for an invalid meetup body
        """
        self.meetup_data['body'] = '#?-234+34```'
        response = self.create_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get(
            'error'), '#?-234+34``` is not a valid meetup body')

    def test_invalid_meetup_location(self) -> None:
        """
        Tests for invalid meetup location input
        """
        self.meetup_data['location'] = '%23...*&^^^'
        response = self.create_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get(
            'error'), '%23...*&^^^ is not a valid meetup location')

    def test_invalid_image_url(self) -> None:
        """
        Tests for an invalid image url for meetup
        """
        self.meetup_data['images'] = ['InvalidUrl']
        response = self.create_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get(
            'error'), 'InvalidUrl is not a valid image url')

    def tes_past_meetup_date(self) -> None:
        """
        Tests scheduling of meetup dates on a passed daye
        """
        self.meetup_data['scheduled_date'] = '2019-03-04 06:00Z'
        response = self.create_meetup()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestViewMeetups(TestSetUp):
    """
    Tests for viewing meetups
    """

    def setUp(self):
        super().setUp()
        self.meetup_id = str(Meetup.objects.all()[0].id)

    def test_all_meetups_response_status(self) -> None:
        """
        Tests for the fetching of all meetups from the database
        """
        response = self.get_all_meetups()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_meetups_not_found(self) -> None:
        """
        Tests for no meeetups existing in the database
        """
        self.clear_meetups()
        response = self.get_all_meetups()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_meetup_id(self) -> None:
        """
        Tests for invalid meetup id
        """
        meetup_id = '390239202SFHEIFHJHH'
        response = self.get_specific_meetup(meetup_id=meetup_id)
        self.assertEqual(response.data.get('error'),
                         'A meetup with that id does not exist')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_specific_meetup(self) -> None:
        """
        Tests fetching of a specific meetup
        """
        response = self.get_specific_meetup(meetup_id=self.meetup_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_number_meetups(self) -> None:
        """
        Tests the number of meetups returned when specific meetup endpoint
        """
        response = self.get_specific_meetup(meetup_id=self.meetup_id)
        self.assertEqual(len(response.data.get('data')), 1)

    def test_zero_upcoming_meetups(self) -> None:
        """
        Tests zero upcoming meetups
        """
        self.clear_meetups()
        response = self.get_upcoming_meetups()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('error'),
                         'There are no upcoming meetups')

    def test_get_upcoming_status(self) -> None:
        """
        Tests status when upcoming meetups are successfully made
        """
        response = self.get_upcoming_meetups()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_past_meetups_inclusion(self) -> None:
        """
        Test if past meetups are included in upcoming meetups
        """
        self.clear_meetups()
        Meetup.objects.create(
            title='Cauchy Linear Homogenous Equations',
            body='Time to meet the authors of logic',
            location='JKUAT',
            scheduled_date=timezone.now()+timezone.timedelta(days=-3),
            creator=self.admin
        )
        response = self.get_upcoming_meetups()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tes_page_limit_upcomint_meetups(self) -> None:
        """
        Tests page limiting in upcoming meetups
        """
        self.upcoming_meetups_url = self.upcoming_meetups_url+'?page_limit=5'
        response = self.get_upcoming_meetups()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pagination_all_meetups(self):
        """
        Tests page limiting in all meetups
        """
        self.all_meetups_url = self.all_meetups_url+'?page_limit=1'
        response = self.get_all_meetups()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRsvpModel(TestCase):
    """
    Test for the Rsvp model
    """

    def setUp(self):
        """
        Setting up
        """
        self.client = APIClient()
        self.user = User.objects._create_user(
            name="Escobar Miguel",
            email="admin@questioner.com",
            password="@Escobar123"
        )
        self.user.is_active = True
        self.user.save()

        self.admin = User.objects._create_user(
            name="Admin User",
            email="admin@help.com",
            password="@Admin123"
        )
        self.user.is_active = True
        self.is_admin = True
        self.user.save()

        self.meetup = Meetup.objects.create(
            title='Test Driven Development',
            body='Developers need to discusss the correct approach of doing test driven development',
            location='Andela Campus',
            creator=self.admin,
            scheduled_date=timezone.now() + timezone.timedelta(days=3)
        )
        self.meetup.save()

    def login_user(self, email="admin@questioner.com", password="@Escobar123"):
        """
        Login in a user to get the token
        """
        url = reverse("user_login")
        data = self.client.post(
            url,
            data=json.dumps({
                "email": email,
                "password": password
            }),
            content_type="application/json"
        )
        res = data.data['token']

        return res

    def test_post_rsvp(self):
        """
        Post rsvp specific to a meetup
        """
        meetup_id = str(self.meetup.id)
        url = reverse('rsvp', args=[meetup_id])
        response = self.client.post(
            url,
            data=json.dumps({
                "response": "Yes"
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_rsvp_without_response(self):
        """
        Post rsvp specific to a meetup with no response
        """
        meetup_id = str(self.meetup.id)
        url = reverse('rsvp', args=[meetup_id])
        res = self.client.post(
            url,
            data=json.dumps({
                "response": ""
            }),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestGetRsvos(TestSetUp):
    """
    Class for testing fetching Rsvps
    """

    def setUp(self):
        super().setUp()
        self.meetup = Meetup.objects.all()[0]
        self.rsvps_url = '/api/meetups/{}/rsvps'.format(self.meetup.id)
        self.invalid_rsvps_url = '/api/meetups/acdd922a-f1ac-4fad-9ed7-fa1013007edb/rsvps'
        self.rsvp = Rsvp.objects.create(
            meetup=self.meetup,
            responder=self.user,
            response='yes',
        )

    def get_rsvps_on_meetup(self, meetup_url: str) -> Response:
        """
        A method for getting rsvps on a meetup
        """
        response = self.client.get(
            path=meetup_url,
            format='json'
        )
        return response

    def test_invalid_meetup_id(self) -> None:
        """
        Tests invalid meetup id in the url
        """
        response = self.get_rsvps_on_meetup(meetup_url=self.invalid_rsvps_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'),
                         'The meetup id is invalid')

    def test_unvaliable_rsvps(self):
        """
        Tests unvailable rsvps on a meetup
        """
        [rsvp.delete() for rsvp in Rsvp.objects.all()]
        response = self.get_rsvps_on_meetup(meetup_url=self.rsvps_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('error'),
                         'There are no rsvps for the meetup')

    def test_successful_rsvp_fetch(self):
        """
        Tests successful fetch of rsvps on a meetup
        """
        response = self.get_rsvps_on_meetup(meetup_url=self.rsvps_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
