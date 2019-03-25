"""
Views operations for the answers
"""
from django.shortcuts import get_object_or_404, _get_queryset
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from rest_framework.views import APIView, Response
from rest_framework.request import Request
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.pagination import PageNumberPagination

from .models import Answer, AnswerVote
from questions.models import Question
from meetups.models import Meetup
from .serializers import AnswerSerializer, GetAnswerSerializer, VoteSerializer
from utils.validators import valid_string
from users.serializers import FetchUserSerializer
from utils.token_validation import TokenAllowedPermission



class AnswersPostView(APIView):
    '''
    Views for posting an answer
    '''
    permission_classes = [permissions.IsAuthenticated, TokenAllowedPermission]

    def post(self, request, questionId, meetupId):
        '''
        Post an answer
        '''
        try:
            queryset = Meetup.objects.get(id=meetupId)
            try:
                queryset = Question.objects.all()
                request.data['creator'] = request.user
                serializer = AnswerSerializer(data=request.data)
                answer_body = Answer.objects.filter(
                    body=request.data.get('body'))

                if valid_string(request.data.get('body')) == False:
                    return Response(
                        {
                            'error': 'Please enter a valid answer'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if serializer.is_valid():
                    if answer_body:
                        return Response(
                            {
                                'error': 'Answer already exist'
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    Answer.objects.update_or_create(
                        body=request.data.get('body').strip(),
                        defaults={
                            'question': get_object_or_404(queryset, id=questionId),
                            'creator': request.data.get('creator')
                        }
                    )
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ValidationError:
                return Response(
                    {
                        'error': 'Question does not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        except ValidationError:
            return Response(
                {
                    'error': 'Meetup does not exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )


class GetAnswerView(APIView):
    """
    We can see all the answers from users in a question
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, meetupId, questionId):
        """
        Get all available answers
        """
        try:
            Meetup.objects.get(id=meetupId)
            try:
                question = Question.objects.filter(id=questionId, meetup=meetupId)
                if question:
                    answer = Answer.objects.filter(question=questionId)
                    if answer:
                        page_limit = request.GET.get('page_limit')
                        if not page_limit:
                            page_limit = 10
                        pagination_class = PageNumberPagination()
                        pagination_class.page_size = page_limit
                        page = pagination_class.paginate_queryset(answer, request)
                        serializer = GetAnswerSerializer(page, many=True)
                        paginated_response = pagination_class.get_paginated_response(serializer.data)
                        return paginated_response
                    return Response(
                        {
                            'error': 'There are no answers in given question'
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
            except:
                return Response(
                    {
                        'error': 'Question does not exist in given meetup'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        except:
            return Response(
                {
                    'error': 'Meetup does not exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )


class UpdateAnswer(APIView):
    """
    Deals with updating a specific answer
    """
    permission_classes = [permissions.IsAuthenticated, TokenAllowedPermission]

    def put(self, request, meetupId, questionId, answerId):
        try:
            queryset = Meetup.objects.get(id=meetupId)
        except ValidationError:
            error = {'error': 'The specified meetup does not exist'}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)

        try:
            Question.objects.filter(id=questionId, meetup=meetupId)
            queryset = Question.objects.get(id=questionId)
        except ValidationError:
            error = {'error': 'The specified question does not exist'}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)

        try:
            Answer.objects.filter(id=answerId, question=questionId)
            answer = Answer.objects.get(id=answerId)
            userid = request.user.id
            if userid != answer.creator.id:
                response = Response(data={'error': 'You cannot edit this answer. You did not post it'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            elif valid_string(request.data.get('body')) == False:
                response = Response(data={'error': 'Please enter a valid answer'},
                                    status=status.HTTP_400_BAD_REQUEST
                                    )
            elif userid == answer.creator.id:
                qs = Answer.objects.filter(
                    body=request.data.get('body'))
                qs = qs.exclude(pk=answer.id)
                if qs.exists():
                    return Response(
                        data={'Error': 'That answer already exists'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)
                newbody = request.data.get('body').strip()
                answer.body = newbody
                answer.save()
                serializer = AnswerSerializer(answer)
                context = {
                    'message': 'You have successfully updated the answer',
                    'data': serializer.data
                }
                response = Response(
                    data=context,
                    status=status.HTTP_201_CREATED
                )
            return response

        except ValidationError:
            error = {'error': 'The specified answer does not exist'}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)


class DeleteAnswer(APIView):
    """
    Class to delete a specific answer
    """
    permission_classes = [permissions.IsAuthenticated, TokenAllowedPermission]

    def delete(self, request, meetupId, questionId, answerId):
        """
        Endpoint to deleting specific answer
        Delete /api/meetups/{meetupId}/questions/{questionId}/answers/{answerId}/
        """
        try:
            meetid = Meetup.objects.get(id=meetupId)
        except  (ObjectDoesNotExist, ValidationError) as e:
            error = {'error': str(e)}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)

        try:
            questionid = Question.objects.get(id=questionId)
        except  (ObjectDoesNotExist, ValidationError) as e:
            error = {'error': str(e)}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)

        try:
            answer = Answer.objects.get(id=answerId)
            is_authenticated = request.user
            owner = Answer.objects.filter(
                creator_id=is_authenticated).first()
            adminuser = request.user.is_staff
            user_superuser =request.user.is_superuser

            if user_superuser or adminuser or owner:
                answer.delete()
                response = Response(data={'message': 'succefully deleted.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                response = Response(data={'error': 'only the admin or user who posted the answer can delete it.'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            return response

        except (ObjectDoesNotExist, ValidationError) as e:
            error = {'error': str(e)}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)


class UpvoteAnswer(APIView):
    """
    View for upvoting answer
    """
    permission_classes = [permissions.IsAuthenticated, TokenAllowedPermission]

    def patch(self, request, meetupId, questionId, answerId):
        """
        Upvote an answer
        """
        message = "Answer Upvoted successfully!"
        vote_choice = "upvote"
        upvoting = user_vote(request, meetupId, questionId, answerId, vote_choice, message)
        return upvoting


class DownvoteAnswer(APIView):
    """
    View for downvoting answer
    """
    permission_classes = [permissions.IsAuthenticated, TokenAllowedPermission]

    def patch(self, request, meetupId, questionId, answerId):
        """
        Downvote an answer
        """
        message = "Answer Downvoted successfully!"
        vote_choice = "downvote"
        downvoting = user_vote(request, meetupId, questionId, answerId, vote_choice, message)
        return downvoting


def user_vote(request, meetupId, questionId, answerId, vote_choice, message):
        """
        vote for an answer
        """
        try:
            meetup = Meetup.objects.get(id=meetupId)
            try:
                question = Question.objects.filter(id=questionId, meetup=meetupId)
                if not question:
                    return Response(
                        data={
                            "error": "Question not in given meetup"
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
                try:
                    answer = Answer.objects.filter(id=answerId, question=questionId)
                    if answer:
                        user = request.user
                        vote = AnswerVote.objects.filter(answer=answerId, creator=user,
                                                         vote_type=vote_choice)
                        if vote:
                            return Response(
                                data={
                                    "error": "You cannot {} an answer more than once".format(vote_choice)
                                },
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        userVote, created = AnswerVote.objects.update_or_create(
                            creator=user,
                            answer=Answer.objects.get(id=answerId),
                            defaults={
                                "vote_type": vote_choice
                            }
                        )
                        upvotes = AnswerVote.objects.filter(answer=answerId,
                                                            vote_type='upvote').count()
                        downvotes = AnswerVote.objects.filter(answer=answerId,
                                                              vote_type='downvote').count()
                        total = upvotes-downvotes
                        voter = FetchUserSerializer(userVote.creator.__dict__, many=False).data
                        return Response(
                                data={
                                    "user": voter,
                                    "answer": userVote.answer.body,
                                    "vote_type": userVote.vote_type,
                                    "upvotes": upvotes,
                                    "downvotes": downvotes,
                                    "vote_score": total,
                                    "message": message
                                },
                                status=status.HTTP_201_CREATED
                            )
                    return Response(
                            data={
                                "error": "Answer not in given question"
                            },
                            status=status.HTTP_404_NOT_FOUND
                        )
                except:
                    return Response(
                        data={
                            "error": "Answer does not exist"
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
            except:
                return Response(
                    data={
                        "error": "Question does not exist"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        except:
            return Response(
                data={
                    "error": "Meetup does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
