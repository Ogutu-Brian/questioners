from rest_framework import status

from .basetests import BaseTest
from questions.models import Question
import json

class QuestionModelTest(BaseTest):
    """
    Tests for questions creation model
    """

    def test_saving_question(self):
        """
        Test if the models are saving data into the database
        """
        new_count = Question.objects.all().count()
        self.assertEqual(new_count, 1)


class PostQuestionTest(BaseTest):
    """
    Tests for questions creation endpoint
    """

    def test_posting_question(self):
        """
        Test successful creation of question
        """
        self.is_authenticated()
        response = self.post_question()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_is_unauthenticated(self):
        """
        Test posting a question while unauthenticated
        """
        response = self.post_question()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_title(self):
        """
        Test posting question without a title
        """
        self.is_authenticated()
        response = self.post_without_title()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_body(self):
        """
        Test posting question without a body
        """
        self.is_authenticated()
        response = self.post_without_body()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_questions(self):
        """
        Test posting of duplicate questions on the same meetup
        """
        self.is_authenticated()
        self.post_question()
        response = self.post_question()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_with_invalid_meetup(self):
        """
        Test posting question with a meetup that does not exist
        """
        self.is_authenticated()
        response = self.post_with_invalid_meetup()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_special_characters(self):
        """
        Test posting special characters
        """
        self.is_authenticated()
        response = self.post_special_characters()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You cannot post special characters")

class ViewQuestionTest(BaseTest):
    """
    Tests for viewing questions posted on meetups
    """

    def test_getting_question_with_valid_meetup_id(self):
        """
        Test view questions with valid meetup_id
        """
        response = self.get_questions_with_valid_meetup_id()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_geeting_meetups_with_no_questions(self):
        """
        Test viewing questions with valid meetup_id but no questions_posted
        """
        response = self.get_question_with_invalid_meetup()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content,
                         b'{"error":"There are no questions"}')

class ViewOneQuestionTest(BaseTest):
    """
    Tests for viewing one question for a specific meetup
    """

    def test_getting_one_question_with_valid_meetup(self):
        """
        Test view one question with valid meetup
        """
        response = self.get_one_question_with_valid_meetup()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_one_question_with_no_meetup(self):
        """
        Test viewing questions with valid meetup_id but no questions_posted
        """
        response = self.get_one_question_with_invalid_meetup()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_getting_one_question_with_invalid_questionId(self):
        """
        Test viewing questions with valid meetup_id but no questions_posted
        """
        response = self.get_one_question_with_invalid_questionId()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        