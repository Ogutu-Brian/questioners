import json
import responses
import re
import os

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from django.utils import timezone

from datetime import datetime

from questions.models import Question
from meetups.models import Meetup
from users.models import User
# Create your tests here.

class BaseTest(APITestCase):
    """
    The base where are default test case settings kept
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects._create_user(
            name="Abraham Kamau",
            email="admin@questioner.com",
            password="@Admin123"
        )
        self.user.is_active = True
        self.user.is_admin = True
        self.user.save()

        self.meetup = Meetup.objects.create(
            title='Test Driven Development',
            body='Developers need to discusss the correct approach of doing test driven development',
            location='Andela Campus',
            creator=self.user,
            scheduled_date=timezone.now() + timezone.timedelta(days=3)
            )
        self.meetup.save()

        self.question = Question.objects.create(
            title="Why are we testing models",
            body="We test models cause we also want to know if the are working",
            meetup=self.meetup,
            created_by=self.user
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
    def is_authenticated(self):
        """Authenticate user before posting data
        """
        token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def post_question(self):
        """
        Post question specific to a meetup
        """
        meetup_id = str(self.meetup.id)
        url = reverse('question', args=[meetup_id])
        response = self.client.post(
            url,
            data = json.dumps({
                "title": "Why are we testing views",
                "body": "We test models cause we also want to know if the are working"
            }),
            content_type="application/json"
        )
        return response
    def post_without_title(self):
        """
        Post question without a title
        """
        meetup_id = str(self.meetup.id)
        url = reverse('question', args=[meetup_id])
        response = self.client.post(
            url,
            data=json.dumps({
                "title": "",
                "body": "We test models cause we also want to know if the are working"
            }),
            content_type="application/json"
        )
        return response

    def post_without_body(self):
        """
        Post question without body
        """
        meetup_id = str(self.meetup.id)
        url = reverse('question', args=[meetup_id])
        response = self.client.post(
            url,
            data=json.dumps({
                "title": "Why are we testing models",
                "body": ""
            }),
            content_type="application/json"
        )
        return response
    def post_with_invalid_meetup(self):
        """
        Post question to invalid meetup
        """
        meetup_id = "f1d63c02-039d-4bdf-806b-45c698f47c3b"
        url = reverse('question', args=[meetup_id])
        response = self.client.post(
            url,
            data=json.dumps({
                "title": "Why are we testing views with invalid meetup",
                "body": "We test models cause we also want to know if the are working"
            }),
            content_type="application/json"
        )
        return response

    def get_questions_with_valid_meetup_id(self):
        """
        Post question to invalid meetup
        """
        meetup_id = str(self.meetup.id)
        url = reverse('view_questions', args=[meetup_id])
        response = self.client.get(url)
        return response

    def get_question_with_invalid_meetup(self):
        """
        view question to invalid meetup
        """
        meetup_id = "f1d63c02-039d-4bdf-806b-45c698f47c3b"
        url = reverse('view_questions', args=[meetup_id])
        response = self.client.get(url)
        return response

    def get_question_with_invalid_uuid(self):
        """
        view question to invalid meetup uuid
        """
        meetup_id = "f"
        url = reverse('view_questions', args=[meetup_id])
        response = self.client.get(url)
        return response
