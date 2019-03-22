import json
import responses
import re
import os

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import User

from datetime import datetime

from questions.models import Question
from meetups.models import Meetup
from answers.models import Answer
from users.models import User

URL_LOGIN = api_reverse("user_login")

class BaseTest(APITestCase):
    """
    basetest
    """

    def setUp(self):
        """
        setup
        """
        self.client = APIClient()

        self.user = User.objects._create_user(
            name="Dude",
            email="dude@gmail.com",
            password="dude@password"
        )
        self.user.is_active = True
        self.user.is_admin = True
        self.user.save()

        self.data_login = {
            "email": "dude@gmail.com",
            "password": "dude@password"
        }
        self.data_login2 = {
            "email": "polo@gmail.com",
            "password":"polo@gmail.com"
        }
        self.user2 = User.objects.create_user(
            name="polo",
            email="polo@gmail.com",
            password="polo@gmail.com"
        )
        self.user2.is_active = True
        self.user2.is_admin = False
        self.user2.save()

        self.meetup = Meetup.objects.create(
            title='Test TiTle',
            body='Test body',
            location='Test location',
            creator=self.user,
            scheduled_date=timezone.now() + timezone.timedelta(days=3)
        )
        self.meetup.save()

        self.question1 = Question.objects.create(
            title="test Title Question",
            body="Test body Question",
            meetup=self.meetup,
            created_by=self.user
        )
        self.question1.save()
        self.answer = Answer.objects.create(
            body="test answer",
            creator=self.user,
            question=self.question1
        )
        self.answer.save()
        self.delete_url = '/api/meetups/'
        
        
        self.meetupId = str(self.meetup.id)
        self.questionId = str(self.question1.id)
        self.answerId = str(self.answer.id)
        self.invalid_answerId = str(1)
        self.invalid_questionId = str(67)
       
    def is_authenticated(self):
        '''
        Authenticate user
        '''
        response = self.client.post(URL_LOGIN, self.data_login2, format='json')
        token = response.data.get("token", None)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def is_authenticated_user2(self):
        '''
        Authenticate user
        '''
        response = self.client.post(URL_LOGIN, self.data_login, format='json')
        token = response.data.get("token", None)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)    


class DeleteAnswer(BaseTest):
    """
    Tests answer Delete functionality
    """
    def test_delete_answer_successfully(self):
        '''
        test delete answer succesfully
        '''
        self.is_authenticated_user2()
        response = self.client.delete(path=self.delete_url+self.meetupId +'/questions/'+self.questionId+'/answers/'+self.answerId+'/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_answer_not_owned_by_user(self):
        '''
        test delete answer not owned by user
        '''
        self.is_authenticated()
        response = self.client.delete(path=self.delete_url+self.meetupId +'/questions/'+self.questionId+'/answers/'+self.answerId+'/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'only the admin or user who posted the answer can delete it.')

    def test_delete_meetid_notfound(self):
        '''
        test for delete meetup id notfound
        '''
        self.is_authenticated()
        [meetup.delete() for meetup in Meetup.objects.all()]
        response = self.client.delete(path=self.delete_url+self.meetupId +'/questions/'+self.questionId+'/answers/'+self.answerId+'/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_invalid_answerid(self):
        '''
        test delete invalid answer id
        '''
        self.is_authenticated()
        response = self.client.delete(path=self.delete_url+self.meetupId +'/questions/'+self.questionId+'/answers/'+self.invalid_answerId+'/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_invalid_questionid(self):
        '''
        test delete inavlid question id
        '''
        self.is_authenticated()
        response = self.client.delete(path=self.delete_url+self.meetupId +'/questions/'+self.invalid_questionId+'/answers/'+self.answerId+'/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        