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
        self.is_authenticated()
        response = self.post_answer()
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
        self.is_authenticated()
        response = self.post_answer()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)