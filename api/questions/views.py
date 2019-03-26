from django.shortcuts import render, get_object_or_404, _get_queryset
from django.core.exceptions import ValidationError
from utils.validators import valid_question
from rest_framework import permissions, status
from rest_framework.views import APIView, Response, Request
from rest_framework.pagination import PageNumberPagination
from questions.models import Question, QuestionVote
from questions.serializers import QuestionsSerializer, ViewQuestionsSerializer, UpdateQuestionSerializer
from meetups.models import Meetup
from utils.validators import valid_string
from users.serializers import FetchUserSerializer


class QuestionViews(APIView):
    """
    View class for performing CRUD operations on questions
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id=None):
        """
        Endpoint for posting questions
        """
        try:
            queryset = Meetup.objects.all()
            request.data['created_by'] = request.user
            serializer = QuestionsSerializer(data=request.data)
            q_title = Question.objects.filter(title=request.data.get('title'))
            q_body = Question.objects.filter(body=request.data.get('body'))
            if serializer.is_valid():
                if q_title and q_body:
                    return Response({
                        "error": "Question already exist"
                    }, status=status.HTTP_400_BAD_REQUEST)
                title_input = valid_string(request.data.get('title'))
                body_input = valid_string(request.data.get('body'))
                if title_input == True and body_input == True:
                    Question.objects.update_or_create(
                        title=request.data.get('title').strip(),
                        body=request.data.get('body').strip(),
                        defaults={
                            'meetup': get_object_or_404(queryset, id=id),
                            'created_by': request.data.get('created_by')
                        }
                    )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({"error": "You cannot post special characters"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            message = str(e)
            return Response({
                "error": message
            }, status=status.HTTP_404_NOT_FOUND)


class QuestionEditViews(APIView):
    """
    class to edit question posted
    /api/meetups/{meetup_id}/questions/{question_id}/
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id, m_id):
        is_valid_question, errors = valid_question(request)
        if is_valid_question:
            try:
                queryset = Meetup.objects.get(id=m_id)
            except ValidationError:
                error = {'error': 'The specified meetup does not exist'}
                return Response(data=error, status=status.HTTP_404_NOT_FOUND)
            try:
                queryset = Question.objects.get(id=id)
            except ValidationError:
                error = {'error': 'The specified question does not exist'}
                return Response(data=error, status=status.HTTP_404_NOT_FOUND)
            try:
                question = Question.objects.get(id=id)
                owner = question.created_by
                if owner.id == request.user.id:

                    obj = Question.objects.get(id=id)
                    u_title = Question.objects.filter(
                        title=request.data.get('title'))
                    u_body = Question.objects.filter(
                        body=request.data.get('body'))
                    if request.data.get('title'):
                        if u_title:
                            return Response({
                                "message": "Question title is upto date"
                            }, status=status.HTTP_400_BAD_REQUEST)
                        newtitle = request.data.get('title').strip()
                        obj.title = newtitle
                    if request.data.get('body'):
                        if u_body:
                            return Response({
                                "message": "Question body upto date"
                            }, status=status.HTTP_400_BAD_REQUEST)
                        newbody = request.data.get('body').strip()
                        obj.body = newbody
                    obj.save()
                    serializer = UpdateQuestionSerializer(obj)
                    context = {
                        'message': 'You have successfully updated the question',
                        'data': serializer.data
                    }
                    return Response(
                        data=context,
                        status=status.HTTP_201_CREATED
                    )
                return Response({
                    "error": "You are not the owner of this question"
                }, status=status.HTTP_401_UNAUTHORIZED)
            except ValidationError as e:
                response = Response({
                    "error": str(e)
                }, status=status.HTTP_404_NOT_FOUND)
        response = Response(
            data=errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        return response

    def delete(self, request, id=None, m_id=None):
        try:
            request.data['created_by'] = request.user
            is_authenticated = request.user
            owner = Question.objects.filter(
                created_by_id=is_authenticated).first()
            meetup = Meetup.objects.filter(id=m_id).first()
            meetup_id = Question.objects.filter(meetup_id=m_id).first()
            try:
                question = Question.objects.filter(id=id).first()
                if not meetup_id:
                    response = Response({
                        "error": "The meetup with that id does not match the question"
                    }, status=status.HTTP_404_NOT_FOUND)
                elif not question:
                    response = Response({
                        "error": "The question does not exist in the database"
                    }, status=status.HTTP_404_NOT_FOUND)
                elif not owner:
                    response = Response({
                        "error": "You are not the owner of this question"
                    }, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    question.delete()
                    response = Response({
                        "message": "Question deleted successfully"
                    }, status=status.HTTP_200_OK)
            except ValidationError:
                response = Response({
                    "error": "That question does not exist"
                }, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            response = Response({
                "error": "That meetup does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

        return response


class ViewQuestionsView(APIView):
    """
    A view for fetching questions specific to a meetup
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, id=None):
        """
        Endpoint for fetching all questions specific to the meetup id specified
        """
        questions = Question.objects.filter(meetup_id=id)
        if questions:
            page_limit = request.GET.get('page_limit')
            if not page_limit:
                page_limit = 10
            pagination_class = PageNumberPagination()
            pagination_class.page_size = page_limit
            page = pagination_class.paginate_queryset(questions, request)
            serializer = ViewQuestionsSerializer(page, many=True)
            paginated_response = pagination_class.get_paginated_response(
                serializer.data)
            return paginated_response
        else:
            response = Response({
                'error': 'There are no questions'
            }, status=status.HTTP_404_NOT_FOUND)
        return response


def give_vote(request: Request, meetup_id: str, question_id: str, vote_value: int) -> Response:
    """
    A function to handle voting
    """
    response = None
    try:
        meetup = Meetup.objects.get(id=meetup_id)
        try:
            question_query = Question.objects.filter(
                id=question_id, meetup=meetup)
            if not question_query:
                response = Response(
                    data={
                        'error': 'The meetup does not have a question with that id'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                question = question_query[0]
                user = request.user
                if QuestionVote.objects.filter(user=user, question=question, vote=vote_value):
                    if vote_value == 1:
                        error_message = 'You cannot upvote a question more than once'
                    else:
                        error_message = 'You cannot downvote a question more than once'
                    response = Response(
                        data={
                            'error': error_message
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    vote, created = QuestionVote.objects.update_or_create(
                        question=question,
                        user=user,
                        defaults={
                            'vote': vote_value
                        },
                    )
                    upvotes = QuestionVote.objects.filter(
                        question=question, vote__gte=1).count()
                    downvotes = QuestionVote.objects.filter(
                        question=question, vote__lt=1).count()
                    votes = upvotes-downvotes
                    voter = FetchUserSerializer(
                        vote.user.__dict__, many=False).data
                    if created:
                        response = Response(
                            data={
                                'data':
                                [{
                                    'question_id': vote.question.id,
                                    'question_title': vote.question.title,
                                    'question_body': vote.question.body,
                                    'upvotes': upvotes,
                                    'downvotes': downvotes,
                                    'vote_score': votes,
                                    'voter': voter
                                }],
                                'message': 'Vote submitted sucessfully'
                            },
                            status=status.HTTP_201_CREATED
                        )
                    else:
                        response = Response(
                            data={
                                'data':
                                [{
                                    'question_id': vote.question.id,
                                    'question_title': vote.question.title,
                                    'question_body': vote.question.body,
                                    'upvotes': upvotes,
                                    'downvotes': downvotes,
                                    'vote_score': votes,
                                    'voter': voter
                                }],
                                'message': 'You have successfully updated your vote'
                            },
                            status=status.HTTP_201_CREATED
                        )
        except:
            response = Response(
                data={
                    'error': 'A question with that id does not exist'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    except:
        response = Response(
            data={
                'error': 'A meetup with that id does not exist'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    return response


class UpvoteQuestion(APIView):
    """
    A viw for handling question upvotes
    PATCH /api/meetups/{meetupId}/questions/{questionId}/upvote
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request: Request, meetup_id: str, question_id: str) -> Response:
        """
        upvote view function 
        """
        vote_value = 1
        return give_vote(
            request=request,
            meetup_id=meetup_id,
            question_id=question_id,
            vote_value=vote_value
        )


class DownvoteQuestion(APIView):
    """
    class to handle downvotes of questions
    PATCH /api/meetups/{meetupId}/questions/{questionId}/downvote
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request: Request, meetup_id: str, question_id: str) -> Response:
        """
        upvote view function 
        """
        vote_value = -1
        return give_vote(
            request=request,
            meetup_id=meetup_id,
            question_id=question_id,
            vote_value=vote_value
        )


class ViewSpecificQuestionView(APIView):
    """
    Class for viewing specific question
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, m_id=None, id=None):
        """
        Endpoint for fetching a specific question to the meetup id specified
        """
        try:
            meetup = Meetup.objects.filter(id=m_id).first()
        except ValidationError:
            data = {'error': 'The specified meetup does not exist'}
            return Response(data, status.HTTP_404_NOT_FOUND)
        try:
            meetup_id = Question.objects.filter(meetup_id=m_id).first()
            if meetup_id:
                question = Question.objects.filter(id=id).first()
                if question:
                    serializer = ViewQuestionsSerializer(question)
                    return Response({'question': serializer.data}, status.HTTP_200_OK)
                return Response({
                    "error": "That question is not found"
                }, status=status.HTTP_404_NOT_FOUND)
            return Response({
                "error": "There are no questions for that meetup"
            }, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            data = {'error': 'The specified question does not exist'}
            return Response(data, status.HTTP_404_NOT_FOUND)
