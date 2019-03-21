from rest_framework import status
from rest_framework.authtoken.models import Token

from .basetests import BaseTest
from questions.models import Question

class QuestionModelTest(BaseTest):
    """
    Tests for questions creation model
    """

    def test_delete_question(self):
        """
        Test if the models are saving data into the database
        """
        self.question.delete()
        new_count = Question.objects.all().count()
        self.assertEqual(new_count, 0)

class DeleteQuestionTest(BaseTest):
    """
    Test for deleting question
    """
    def test_deleting_question(self):
        """
        Test successful deletion of question
        """
        self.is_authenticated()
        response = self.delete_question()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_is_unauthenticated(self):
        """
        Test deleting a question while unauthenticated
        """
        response = self.delete_question()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_invalid_question(self):
        """
        Test deleting a question that does not exist
        """
        self.is_authenticated()
        response = self.delete_invalid_question()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_with_invalid_meetup(self):
        """
        Test deleting a question with a meetup that does not exist
        """
        self.is_authenticated()
        response = self.delete_with_invalid_meetup()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_with_unmatch_meetup(self):
        """
        Test deleting a question with a meetup that does not match
        """
        self.is_authenticated()
        response = self.delete_with_unmatch_meetup()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_is_not_owner(self):
        """
        Test the user is not owner of the question
        """
        token, created = Token.objects.get_or_create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.delete_question()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED )
        