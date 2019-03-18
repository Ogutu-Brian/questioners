"""
Tests for votes
"""
from meetups.tests.initial_setup import TestSetUp
from questions.models import QuestionVote, Question
from meetups.models import Meetup
import django
from rest_framework.response import Response
from rest_framework import status


class BaseTest(TestSetUp):
    """
    Base test for voting questions
    """

    def setUp(self):
        super().setUp()
        self.meetup = Meetup.objects.all()[0]
        self.meetup_id = self.meetup.id
        self.question = Question.objects.create(
            title='What is that supposed to be',
            body='I was wondering what the meetup is for',
            meetup=self.meetup,
            created_by=self.user
        )
        self.vote = QuestionVote.objects.create(
            vote=1,
            question=self.question,
            user=self.user,
        )
        self.question_id = self.question.id
        self.upvote_url = '/api/meetups/{}/questions/{}/upvote'.format(
            self.meetup_id, self.question_id)
        self.downvote_url = '/api/meetups/{}/questions/{}/downvote'.format(
            self.meetup_id, self.question_id)
        self.specific_question_url = '/api/meetups/{}/questions/{}'.format(
            self.meetup_id, self.question_id)
        self.fake_id = '81eb4aee-b424-4015-8b7e-c55e844fb96a'

    def clear_votes(self) -> None:
        """
        clears all votes that could have been created
        """
        [vote.delete() for vote in QuestionVote.objects.all()]

    def upvote_question(self) -> Response:
        """
        Upvotes a question
        """
        response = self.client.patch(
            path=self.upvote_url,
            format='json'
        )
        return response

    def downvote_question(self) -> Response:
        """
        Downvotes a question
        """
        response = self.client.patch(
            path=self.downvote_url,
            format='json'
        )
        return response

    def upvote(self) -> Response:
        """
        Upvotes question after authentoicating user
        """
        self.force_authenticate_user()
        response = self.upvote_question()
        return response

    def downvote(self) -> Response:
        """
        Authenticates a user and downvotes a question
        """
        self.force_authenticate_user()
        response = self.downvote_question()
        return response

    def get_all_votes(self) -> Response:
        """
        Gets the all votes on a question
        """
        response = self.client.get(
            path=self.specific_question_url,
            format='json'
        )
        return response


class TestVoteModel(BaseTest):
    """
    Tests the vote model
    """

    def test_persistence_in_db(self) -> None:
        """
        Tests if a vote is persistent in the database
        """
        self.clear_votes()
        QuestionVote.objects.create(
            vote=1,
            question=self.question,
            user=self.user,
        )
        num_votes = QuestionVote.objects.all().count()
        self.assertEqual(num_votes, 1)

    def test_multiple_vote(self) -> None:
        """
        Tests if a user can vote more than once to a given vote
        """
        try:
            message = "successfully voted"
            QuestionVote.objects.create(
                vote=1,
                question=self.question,
                user=self.user,
            )
        except django.db.IntegrityError:
            message = 'Error occured during creation of vote'
        finally:
            self.assertEqual(
                'Error occured during creation of vote', message)

    def test_missing_vote_value(self) -> None:
        """
        Tests if a vote without value can be saved in the database
        """
        self.clear_votes()
        try:
            message = "successfully voted"
            QuestionVote.objects.create(
                question=self.question,
                user=self.user,
            )
        except django.db.IntegrityError:
            message = 'Error occured during creation of vote'
        finally:
            self.assertEqual(
                'Error occured during creation of vote', message)

    def test_missing_question(self) -> None:
        """
        Tests if a vote can be cast without a question
        """
        try:
            message = "successfully voted"
            QuestionVote.objects.create(
                vote=1,
                user=self.user,
            )
        except django.db.IntegrityError:
            message = 'Error occured during creation of vote'
        finally:
            self.assertEqual(
                'Error occured during creation of vote', message)

    def test_missing_user(self) -> None:
        """
        Tests if a vote can be saved without a user who gave the vote
        """
        try:
            message = "successfully voted"
            QuestionVote.objects.create(
                vote=1,
                question=self.question,
            )
        except django.db.IntegrityError:
            message = 'Error occured during creation of vote'
        finally:
            self.assertEqual(
                'Error occured during creation of vote', message)


class TestVote(BaseTest):
    def setUp(self):
        super().setUp()

    def test_invalid_upvote_question_id(self) -> None:
        """
        Tests for an invalid question id during upvote
        """
        self.question_id = 'Invalid question id'
        self.upvote_url = '/api/meetups/{}/questions/{}/upvote'.format(
            self.meetup_id, self.question_id)
        response = self.upvote()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'),
                         'A question with that id does not exist')

    def tes_invalid_question_id_downvote(self) -> None:
        """
        Tests invalid downvote question id
        """
        self.question_id = 'Invalid question id'
        self.downvote_url = '/api/meetups/{}/questions/{}/downvote'.format(
            self.meetup_id, self.question_id)
        response = self.downvote()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'),
                         'A question with that id does not exist')

    def test_missing_question_upvote(self) -> None:
        """
        Tests missing question on the meetup
        """
        self.question_id = self.fake_id
        self.upvote_url = '/api/meetups/{}/questions/{}/upvote'.format(
            self.meetup_id, self.question_id)
        response = self.upvote()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'),
                         'The meetup does not have a question with that id')

    def test_missing_question_downvote(self) -> None:
        """
        Tests missing question in downvote
        """
        self.question_id = self.fake_id
        self.downvote_url = '/api/meetups/{}/questions/{}/downvote'.format(
            self.meetup_id, self.question_id)
        response = self.downvote()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'),
                         'The meetup does not have a question with that id')

    def test_invalid_upvote_meetup_id(self) -> None:
        """
        Tests invalid meetup id tp a question
        """
        self.meetup_id = self.fake_id
        self.upvote_url = '/api/meetups/{}/questions/{}/upvote'.format(
            self.meetup_id, self.question_id)
        response = self.upvote()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'),
                         'A meetup with that id does not exist')

    def invalid_downvote_meetup_id(self) -> None:
        """
        tests invalid upvote meetup id
        """
        self.meetup_id = self.fake_id
        self.downvote_url = '/api/meetups/{}/questions/{}/downvote'.format(
            self.meetup_id, self.question_id)
        response = self.downvote()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'),
                         'A meetup with that id does not exist')

    def test_unauthenticated_user_upvote(self) -> None:
        """
        Tests if unauthenticated_user can upvote
        """
        response = self.upvote_question()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_downvote(self) -> None:
        """
        Tests if unautheticated user can downvote a question
        """
        response = self.downvote_question()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_multiple_upvote(self) -> None:
        """
        Tests multiple upvotes
        """
        self.clear_votes()
        self.upvote()
        response = self.upvote()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'),
                         'You cannot upvote a question more than once')

    def test_multuple_downvote(self) -> None:
        """
        Tests multiple downvote
        """
        self.clear_votes()
        self.downvote()
        response = self.downvote()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'),
                         'You cannot downvote a question more than once')

    def test_upvote_update(self) -> None:
        """
        Tests change of upvote value to downvote
        """
        self.clear_votes()
        self.downvote()
        response = self.upvote()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('message'),
                         'You have successfully updated your vote')

    def test_downvote_update(self) -> None:
        """
        Tests change of downvote value to an upvote
        """
        self.clear_votes()
        self.upvote()
        response = self.downvote()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('message'),
                         'You have successfully updated your vote')

    def test_successful_upvote(self) -> None:
        """
        Tests successful upvote of question
        """
        self.clear_votes()
        response = self.upvote()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('message'),
                         'Vote submitted sucessfully')

    def test_successful_downvote(self) -> None:
        """
        Test successful downvote of question
        """
        self.clear_votes()
        response = self.downvote()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('message'),
                         'Vote submitted sucessfully')

    def test_vote_count(self) -> None:
        """
        Tests the number of vote counts
        """
        self.downvote()
        self.downvote()
        vote_count = QuestionVote.objects.all().count()
        self.assertEqual(vote_count, 1)
