"""
Users endpoint tests
"""
from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse
from django.urls import resolve
from users.models import User

from rest_framework.test import APIClient
from rest_framework import status
from auth.views import (SignUpView, ResendActivationView,
                        ActivationView)


class BaseTestCase(TestCase):
    """
    Sets up the tests for user signup tests
    """

    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse("user_signup")
        self.resend_url = reverse("user_resend")
        self.activate_url = reverse("user_activate")
        self.user = {
            "name": "joaqin",
            "nick_name": "elchapo",
            "email": "jicijobah@freeweb.email",
            "password": "Qwerty123!"
        }
        self.user_two = {
            "name": "pablo",
            "nick_name": "escoba",
            "password": "Qwerty123!"
        }
        self.user_three = {
            "name": "Emmanuela",
            "nick_name": "Angela",
            "email": "jicijobah@freeweb.email"
        }
        self.common_pass = {
            "name": "joaqin",
            "nick_name": "elchapo",
            "email": "elchapo@email.com",
            "password": "qwerty123"
        }
        self.email = {
            "email": "jicijobah@freeweb.email"
        }
        self.wrong_email = {
            "email": "chapo@email.com"
        }        
        self.activation = {
            "uid": "NDIxZjBmMmMtYTI0Zi00OWMyLWJmYjMtNzJmYWNiMzhhNTVj",
            "token": "54f-9c2e1bdaa43dd67441ac"
        }
        self.activation = {
            "uid": "NDIxZjBmMmMtYTI0Zi00OWMyLWJmYjMtNzJmYWNiMzhhNTVj",
            "token": "54f-9c2e1bdaa43dd67441ac"
        }

        self.email_one = 'admin@help.com'
        self.password = 'adminPassw0rd'
        self.new_user = User(email=self.email_one, password=self.password)

    def test_model_can_create_a_user(self):
        """
        Test if user are created
        """
        old_count = User.objects.count()
        self.new_user.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_user_was_saved(self):
        """
        Test if a user can be created
        """
        user = User.objects.create(name="Brian", nick_name="Ogutu",
                                   email="codingbrian58@gmail.com",
                                   password="Henkdebruin58")
        self.assertEqual(user.name, "Brian")
        self.assertEqual(user.email, "codingbrian58@gmail.com")

    def test_create_user(self):
        """
        Test if a user can be created with extra fields
        """
        user = User.objects.create_user(name="Barclay", nick_name="Koin",
                                   email="barclay@koin.com",
                                   password="Henkdebruin58")
        self.assertEqual(user.name, "Barclay")
        self.assertEqual(user.email, "barclay@koin.com")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)

    def test_create_superuser(self):
        """
        Test if a super user can be created with extra fields
        """
        user = User.objects.create_superuser(name="Pablo",
                                   email="pablo@koin.com",
                                   password="Henkdebruin58")
        self.assertEqual(user.name, "Pablo")
        self.assertEqual(user.email, "pablo@koin.com")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)

class TestSignup(BaseTestCase):
    """
    Test User signup
    """

    def test_create_new_account(self):
        """
        Test successful create new user account
        """
        response = self.client.post(self.signup_url, self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert response.data.get("name")

    def test_create_repeat_email(self):
        """
        Test email already registered
        """
        self.client.post(self.signup_url, self.user)
        response = self.client.post(self.signup_url, self.user)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_missing_email(self):
        """
        Test when email is missing
        """
        self.client.post(self.signup_url, self.user_two)
        response = self.client.post(self.signup_url, self.user_two)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data.get("email")

    def test_missing_password(self):
        """
        Test when email is missing
        """
        self.client.post(self.signup_url, self.user_three)
        response = self.client.post(self.signup_url, self.user_three)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data.get("password")

    def test_common_password(self):
        """
        Test register with common password
        """
        response = self.client.post(self.signup_url, self.common_pass)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data.get("password")


class TestResendActivation(BaseTestCase):
    """
    Test Resend activation
    """

    def test_resend_activation(self):
        """
        Test successful resend activation endpoint
        """
        self.client.post(self.signup_url, self.user)
        response = self.client.post(self.resend_url, self.email)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_resend_activation_with_wrong_email(self):
        """
        Test resend activation with non-existent email
        """
        self.client.post(self.signup_url, self.user)
        response = self.client.post(self.resend_url, self.wrong_email)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        assert response.data.get("detail")


class TestUrls(BaseTestCase, SimpleTestCase):
    """
    Test urls are resolved
    """

    def test_signup_url_is_resolved(self):
        """
        Test signup url
        """
        self.assertEqual(resolve(self.signup_url).func.view_class, SignUpView)

    def test_resend_url_is_resolved(self):
        """
        Test resend activation url
        """
        self.assertEqual(resolve(self.resend_url).func.view_class,
                         ResendActivationView)

    def test_activate_url_is_resolved(self):
        """
        Test activation url
        """
        self.assertEqual(resolve(self.activate_url).func.view_class,
                         ActivationView)
