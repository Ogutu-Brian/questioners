from rest_framework import status

from .basetests import BaseTest
from questions.models import Question


class UpdateQuestionTest(BaseTest):
    """
    Tests for updating questions posted
    """

    def test_updating_invalid_questions(self):
        """
        Test updating question with a question id that does not exist/onvalid
        """
        self.is_authenticated()
        response = self.update_invalid_question_id()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.content, b'{"error":"The specified question does not exist"}')

    def test_updating_questions_invalid_meetup(self):
        """
        Test updating question with a qmeetup id that does not exist/on is invalid
        """
        self.is_authenticated()
        response = self.update_invalid_meetup_id()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.content, b'{"error":"The specified meetup does not exist"}')

    def test_editng_question(self):
        """
        Test successful updating of question
        """
        self.is_authenticated()
        response = self.update_question()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],
                         "question updated succesfully")

    def test_update_without_authentication(self):
        """
        Test for updating a question while unauthenticated
        """
        response = self.update_question()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_updating_with_missing_title(self):
        """
        Test updating question and title is missing
        """
        self.is_authenticated()
        response = self.update_without_title()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content,
                         b'{"title":["This field may not be blank."]}')

    def test_update_with_invalid_body(self):
        """
        Test updating questid body 
        """
        self.is_authenticated()
        response = self.update_with_invalid_body()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_with_invalid_title(self):
        """
        Test updating question with invalid title 
        """
        self.is_authenticated()
        response = self.update_with_invalid_title()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_updating_with_missing_body(self):
        """
        Test posting question without a body
        """
        self.is_authenticated()
        response = self.update_without_body()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content,
                         b'{"body":["This field may not be blank."]}')

    def test_update_without_changing_contents(self):
        """
        Test update_without_changing_contents
        """
        self.is_authenticated()
        response = self.update_without_changing_contents()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content,
                         b'{"message":"Question is upto date"}')
