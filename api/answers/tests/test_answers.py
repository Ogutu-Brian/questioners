from rest_framework import status

from .basetests import BaseTest
from answers.models import Answer


class PostAnswerTest(BaseTest):
    """
    Test if an answer can be posted
    """

    def test_unsuccessful_post_answer(self):
        """
        Test 404 question not found
        """
        self.is_authenticated(self.user1)
        response = self.post_answer_without_question()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('error'),
                         self.post_answer_without_question().data.get('error')
                         )

    def test_successful_post_answer(self):
        """
        Test 201 answer created
        """
        self.is_authenticated(self.user1)
        response = self.post_answer()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_successful_get_an_answer(self):
        """
        Test 200 get answer
        """
        self.is_authenticated(self.user1)
        response = self.get_answer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsuccessful_get_an_answer_without_question(self):
        """
        Test 404 get answer with no question
        """
        self.is_authenticated(self.user1)
        response = self.get_answer_without_question()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_answer_if_not_autheticated(self):
        """
        Test posting with un authenticated user (401)
        """
        response = self.post_answer()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unsuccessful_post_answer_to_wrong_meetup(self):
        """
        Test 404 meetup not found
        """
        self.is_authenticated(self.user1)
        response = self.post_answer_with_no_meetup()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unsuccessful_post_answer_with_special_characters(self):
        """
        Test 404 answer is invalid
        """
        self.is_authenticated(self.user1)
        response = self.post_answer_with_special_character()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_post_answer_without_body(self):
        """
        Test 404 answer is invalid
        """
        self.is_authenticated(self.user1)
        response = self.post_answer_without_body()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
