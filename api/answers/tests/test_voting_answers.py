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

        self.user = User.objects._create_user(
            name="Pablo Escobar",
            email="admin@questioner.com",
            password="@Admin123"
        )
        self.user.is_active = True
        self.user.is_admin = True
        self.user.save()

        self.meetup1 = Meetup.objects.create(
            title='Test Driven Development',
            body='Developers need to discusss',
            location='Andela Campus',
            creator=self.user,
            scheduled_date=timezone.now() + timezone.timedelta(days=3)
        )
        self.meetup1.save()

        self.meetup2 = Meetup.objects.create(
            title='Data  science',
            body='Big data',
            location='Nairobi',
            creator=self.user,
            scheduled_date=timezone.now() + timezone.timedelta(days=5)
        )
        self.meetup2.save()

        self.question1 = Question.objects.create(
            title="Why are we testing models",
            body="We test models because",
            meetup=self.meetup1,
            created_by=self.user
        )
        self.question1.save()

        self.question2 = Question.objects.create(
            title="What is data science",
            body="Explain data science",
            meetup=self.meetup2,
            created_by=self.user
        )
        self.question2.save()

        self.answer1 = Answer.objects.create(
            body="test answer",
            creator=self.user,
            question=self.question1
        )
        self.answer1.save()

        self.answer2 = Answer.objects.create(
            body="test data science",
            creator=self.user,
            question=self.question2
        )
        self.answer2.save()

        self.meetupId = str(self.meetup1.id)
        self.questionId = str(self.question1.id)
        self.answerId = str(self.answer1.id)
        self.questionId2 = str(self.question2.id)
        self.answerId2 = str(self.answer2.id)
        self.invalid_id = str(15486558)

    def is_logged_in(self, user):
        """
        Authenticate a user and get the token
        """
        token, created = Token.objects.get_or_create(user=user)
        return self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def upvote_answer(self, meetup, question, answer):
        """
        Upvotes an answer
        """
        url = reverse('upvote_answer', args=[meetup, question, answer])

        response = self.client.patch(
            url,
            content_type="application/json"
        )
        return response

    def downvote_answer(self, meetup, question, answer):
        """
        Downvotes an answer
        """
        url = reverse('downvote_answer', args=[meetup, question, answer])

        response = self.client.patch(
            url,
            content_type="application/json"
        )
        return response


class VoteAnswer(BaseTest):
    """
    Test answer upvote functionality
    """
    def test_upvote_answer_successfully(self):
        self.is_logged_in(self.user)
        response = self.upvote_answer(self.meetupId, self.questionId,
                                      self.answerId)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('upvotes'), 1)

    def test_downvote_answer_successfully(self):
        self.is_logged_in(self.user)
        response = self.downvote_answer(self.meetupId, self.questionId,
                                        self.answerId)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('downvotes'), 1)

    def test_upvote_same_answer_twice(self):
        self.is_logged_in(self.user)
        self.upvote_answer(self.meetupId, self.questionId, self.answerId)
        response = self.upvote_answer(self.meetupId, self.questionId,
                                      self.answerId)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'),
                         'You cannot upvote an answer more than once')

    def test_downvote_same_answer_twice(self):
        self.is_logged_in(self.user)
        self.downvote_answer(self.meetupId, self.questionId, self.answerId)
        response = self.downvote_answer(self.meetupId, self.questionId,
                                        self.answerId)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'),
                         'You cannot downvote an answer more than once')

    def test_meetup_does_not_exist_upvote(self):
        self.is_logged_in(self.user)
        response = self.upvote_answer(self.invalid_id, self.questionId,
                                      self.answerId)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('error'),
                         'Meetup does not exist')

    def test_meetup_does_not_exist_downvote(self):
        self.is_logged_in(self.user)
        response = self.downvote_answer(self.invalid_id, self.questionId,
                                        self.answerId)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('error'),
                         'Meetup does not exist')

    def test_question_does_not_exist_upvote(self):
        self.is_logged_in(self.user)
        response = self.upvote_answer(self.meetupId, self.invalid_id,
                                      self.answerId)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('error'),
                         'Question does not exist')

    def test_question_does_not_exist_downvote(self):
        self.is_logged_in(self.user)
        response = self.downvote_answer(self.meetupId, self.invalid_id,
                                        self.answerId)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('error'),
                         'Question does not exist')

    def test_answer_does_not_exist_upvote(self):
        self.is_logged_in(self.user)
        response = self.upvote_answer(self.meetupId, self.questionId,
                                      self.invalid_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('error'),
                         'Answer does not exist')

    def test_answer_does_not_exist_downvote(self):
        self.is_logged_in(self.user)
        response = self.downvote_answer(self.meetupId, self.questionId,
                                        self.invalid_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('error'),
                         'Answer does not exist')

    def test_question_does_not_exist_in_meetup_upvote(self):
        self.is_logged_in(self.user)
        response = self.upvote_answer(self.meetupId, self.questionId2,
                                      self.answerId)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('error'),
                         'Question not in given meetup')

    def test_question_does_not_exist_in_meetup_downvote(self):
        self.is_logged_in(self.user)
        response = self.downvote_answer(self.meetupId, self.questionId2,
                                        self.answerId)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('error'),
                         'Question not in given meetup')

    def test_answer_does_not_exist_in_question_upvote(self):
        self.is_logged_in(self.user)
        response = self.upvote_answer(self.meetupId, self.questionId,
                                      self.answerId2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('error'),
                         'Answer not in given question')

    def test_answer_does_not_exist_in_question_downvote(self):
        self.is_logged_in(self.user)
        response = self.downvote_answer(self.meetupId, self.questionId,
                                        self.answerId2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('error'),
                         'Answer not in given question')
