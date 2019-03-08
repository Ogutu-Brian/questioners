import json
import responses
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase

from contextlib import contextmanager

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient, APITestCase

from urllib.parse import parse_qs, urlparse
from urllib3_mock import Responses

resps = Responses('requests.packages.urllib3')

from users.models import User

# Create your tests here.

User = get_user_model()
user_data = {
    'id': '001',
    'name': 'Abraham Kamau',
    'email': 'ericabraham806@gmail.com',
}


class BaseTest(APITestCase):
    """
    The base test class for all default test case settings
    """
    client = APIClient
    provider = 'google-oauth2'
    QUERY_STRINGS_RE = '\?([\w-]+(=[\w-]*)?(&[\w-]+(=[\w-]*)?)*)?$'

    base_url = 'https://www.googleapis.com/plus/v1/people/me'.replace(
        '.', r'\.')
    mock_url = re.compile(
        base_url + QUERY_STRINGS_RE
    )

    def login_user(self, email="", password=""):
        url = reverse("user_login")
        return self.client.post(
            url,
            data=json.dumps({
                "email": email,
                "password": password
            }),
            content_type="application/json"
        )

    def save_user(self):
        User.objects.create(
            name="Abraha Kamau",
            nick_name="greean",
            email="ericabraham806@gmail.com",
            password="@Us3r.com"
        )

    def social_login(self, token):
        social_url = reverse("social")
        return self.client.post(
            social_url,
            data=json.dumps({
                "access_token": token,
                "provider": self.provider
            }),
            content_type="application/json"
        )

    def setUp(self):

        self.user = User.objects._create_user(
            nick_name="admin",
            email="admin@questioner.com",
            password="@Admin123"
        )


class LoginTest(BaseTest):
    """
    Tests for auth/login endpoint
    """

    def test_login_correct_credentials(self):
        """
        Test correct user login credentials
        """
        response = self.login_user("admin@questioner.com", "@Admin123")
        self.assertIn("auth_token", response.data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_login_incorrect_credentials(self):
        """
        Test incorrect user login credentials
        """
        response = self.login_user("abraham", "aBu#123")
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)


def generate_resp(request):
    token = parse_qs(urlparse(request.url).query)['access_token'][0]
    status = 200
    try:
        body = user_data[token]
    except KeyError:
        body = {'errors': 'Invalid Token'}
        status = 401
    return (status, {}, json.dumps(body))


@contextmanager
def mocked(endpoint):
    with responses.RequestsMock() as rsps:
        rsps.add_callback(resps.GET, endpoint,
                          callback=generate_resp,
                          content_type='application/json',
                          match_querystring=True,
                          )
        yield rsps


class GoogleOAuthTest(BaseTest):
    """
    Tests for google authentication using OAuth2
    """

    def test_new_user_creation(self):
        "Ensure that we can correctly create a new user for someone with a valid token."
        for token, data in user_data.items():
            with self.subTest(token=token), mocked(self.mock_url):
                response = self.social_login(token)

                self.assertEqual(response.status_code, HTTP_201_CREATED)
                self.assertIn('token', response.data)
                self.assertNotEqual(response.data['token'], token)
                self.assertEqual(User.objects.filter(
                    email=data['email']).count(), 1)

                user_model = User.objects.get(email=data['email'])
                self.assertEqual(user_model.username, user_model.email)

    def test_existing_user_login(self):
        """
        Tests if existing user can login with token
        """
        for token, data in user_data.items():
            self.save_user
            with self.subTest(token=token), mocked(self.mock_url):
                response = self.social_login(token)
                self.assertEqual(response.status_code, HTTP_200_OK)
                self.assertIn('auth_token', response.data)
                self.assertNotEqual(response.data['auth_token'], token)
                self.assertEqual(User.objects.filter(
                    email=data['email']).count(), 1)
                user = User.objects.get(email=data['email'])
                self.assertEqual(user.get_full_name(), data['name'])

    def test_invalid_google_token(self):
        "Ensure that users who present an invalid social token are not granted access"
        emails = {u.email for u in User.objects.all()}

        token = 'invalid_token'
        response = self.social_login(token)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertNotIn('token', response.data)

        new_emails = {u.email for u in User.objects.all()}
        self.assertEqual(emails, new_emails)
