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

        self.answer = Answer.objects.create(
            body="test answer",
            creator=self.user2,
            question=self.question1
        )
        self.answer.save()

        self.answer2 = Answer.objects.create(
            body="test answer body 2",
            creator=self.user1,
            question=self.question1
        )
        self.answer2.save()

        self.update_data = {
            'body':'This is the new test update data'
        }
        self.duplicate_data = {
            'body': 'test answer body 2'
        }
        self.invalid_data = {
            'body': '!@#$%^&*(!@#$%'
        }

        self.meetupId = str(self.meetup.id)
        self.questionId = str(self.question2.id)
        self.answerId = str(self.answer.id)
        self.invalid_id = str(1)
       
    def is_logged_in(self, user):
        """
        Authenticate a user and get the token
        """
        token, created = Token.objects.get_or_create(user=user)
        return self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def update_answer(self, data, meetup, question, answer):
        """
        Updates an answer 
        """
        url = reverse('update_answer', args=[meetup, question, answer])

        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        return response


class UpdateAnswer(BaseTest):
    """
    Tests answer update functionality
    """
    def test_update_answer_successfully(self):
        self.is_logged_in(self.user2)
        response = self.update_answer(self.update_data, self.meetupId, self.questionId, self.answerId)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'You have successfully updated the answer')

    def test_update_existing_answer(self):
        self.is_logged_in(self.user2)
        response = self.update_answer(self.duplicate_data, self.meetupId, self.questionId, self.answerId) 
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data['Error'], 'That answer already exists')

    def test_update_answer_not_owned_by_user(self):
        self.is_logged_in(self.user1)
        response = self.update_answer(self.update_data, self.meetupId, self.questionId, self.answerId)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'You cannot edit this answer. You did not post it')

    def test_update_invalid_answer(self):
        self.is_logged_in(self.user2)
        response = self.update_answer(self.invalid_data, self.meetupId, self.questionId, self.answerId)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Please enter a valid answer')
        
    def test_update_no_meetup(self):
        self.is_logged_in(self.user2)
        response = self.update_answer(self.update_data, self.invalid_id, self.questionId, self.answerId)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'The specified meetup does not exist')

    def test_update_no_question(self):
        self.is_logged_in(self.user2)
        response = self.update_answer(self.update_data, self.meetupId, self.invalid_id, self.answerId)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'The specified question does not exist')
    
    def test_update_no_answer(self):
        self.is_logged_in(self.user2)
        response = self.update_answer(self.update_data, self.meetupId, self.questionId, self.invalid_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'The specified answer does not exist')

    

