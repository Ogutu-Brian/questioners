
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
from answers.models import Answer
from users.models import User
# Create your tests here.


class BaseTest(APITestCase):
    """
    The base where are default test case settings kept
    """

    def setUp(self):
        """
        Basic setup
        """
        self.client = APIClient()

        self.user1 = User.objects._create_user(
            name="Pablo Escobar",
            email="admin@questioner.com",
            password="@Admin123"
        )
        self.user1.is_active = True
        self.user1.is_admin = True
        self.user1.save()

        self.user2 = User.objects.create_user(
            name="Higuen Griazman",
            email="user@questioner.com",
            password="@Users123"
        )
        self.user2.is_active = True
        self.user2.is_admin = False
        self.user2.save()

        self.meetup = Meetup.objects.create(
            title='Test Driven Development',
            body='Developers need to discusss the correct approach of doing test driven development',
            location='Andela Campus',
            creator=self.user2,
            scheduled_date=timezone.now() + timezone.timedelta(days=3)
        )
        self.meetup.save()

        self.question1 = Question.objects.create(
            title="Why are we testing models",
            body="We test models cause we also want to know if the are working",
            meetup=self.meetup,
            created_by=self.user1
        )
        self.question1.save()

        self.question2 = Question.objects.create(
            title="Why are we testing models",
            body="We test models cause we also want to know if the are working",
            meetup=self.meetup,
            created_by=self.user2
        )
        self.question2.save()

        self.question3 = Question.objects.create(
            title="Just making sure",
            body="We test models if the are working",
            meetup=self.meetup,
            created_by=self.user2
        )
        self.question3.save()


    def is_authenticated(self, user):
        """
        Authenticate a user and get the token
        """
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def post_answer(self):
        """
        Post an answer to a specific question
        """
        meetup_id = str(self.meetup.id)
        question_id = str(self.question1.id)
        url = reverse('post_answer', args=[meetup_id, question_id])

        response = self.client.post(
            url,
            data=json.dumps({
                "body": "Will there be food"
            }),
            content_type="application/json"
        )
        return response

    def get_answer(self):
        """
        Get an answer to a specific question
        """
        meetup_id = str(self.meetup.id)
        question_id = str(self.question1.id)
        url = reverse('Get_all_answers', args=[meetup_id, question_id])

        response = self.client.get(
            url,
            content_type="application/json"
        )
        return response

    def post_answer_with_special_character(self):
        """
        Post an answer to a specific question
        """
        meetup_id = str(self.meetup.id)
        question_id = str(self.question1.id)
        url = reverse('post_answer', args=[meetup_id, question_id])

        response = self.client.post(
            url,
            data=json.dumps({
                "body": "!@#$%^&"
            }),
            content_type="application/json"
        )
        return response

    def post_answer_with_no_meetup(self):
        """
        Post an answer to a specific question with no meetup
        """
        meetup_id = str(1)
        question_id = str(self.question1.id)
        url = reverse('post_answer', args=[meetup_id, question_id])

        response = self.client.post(
            url,
            data=json.dumps({
                "body": "Will there be wine"
            }),
            content_type="application/json"
        )
        return response

    def post_answer_without_question(self):
        """
        Post an answer with no question
        """
        meetup_id = str(self.meetup.id)
        question_id = str(2)
        url = reverse('post_answer', args=[meetup_id, question_id])

        response = self.client.post(
            url,
            data=json.dumps({
                "body": "Will there be food"
            }),
            content_type="application/json"
        )
        return response

    def post_answer_without_body(self):
        """
        Post an answer to a specific question
        """
        meetup_id = str(self.meetup.id)
        question_id = str(self.question1.id)
        url = reverse('post_answer', args=[meetup_id, question_id])

        response = self.client.post(
            url,
            data=json.dumps({
                "body": " "
            }),
            content_type="application/json"
        )
        return response

    def get_answer_without_question(self):
        """
        Get an answer to a specific question
        """
        meetup_id = str(1)
        question_id = str(1)
        url = reverse('Get_all_answers', args=[meetup_id, question_id])

        response = self.client.get(
            url,
            content_type="application/json"
        )
        return response