"""
Views operations for the answers
"""
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError ,ObjectDoesNotExist

from rest_framework.views import APIView, Response
from rest_framework.request import Request
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes, api_view

from .models import Answer
from questions.models import Question
from meetups.models import Meetup
from .serializers import AnswerSerializer, GetAnswerSerializer
from utils.validators import valid_string


class AnswersPostView(APIView):
    '''
    Views for posting an answer
    '''
    permission_classes = [permissions.IsAuthenticated]

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
        Get all available RSVP
        """
        try:
            Meetup.objects.get(id=meetupId)
            try:
                Question.objects.filter(id=questionId, meetup=meetupId)
                response = Answer.objects.all()
                serializer = GetAnswerSerializer(response, many=True)
                return Response(
                    {"Answers": serializer.data}
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


class UpdateAnswer(APIView):
    """
    Deals with updating a specific answer
    """
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

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
