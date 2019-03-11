from django.shortcuts import render, get_object_or_404, _get_queryset
from django.core.exceptions import ValidationError

from rest_framework import permissions, status
from rest_framework.views import APIView, Response
from rest_framework.pagination import PageNumberPagination

from questions.models import Question
from questions.serializers import QuestionsSerializer, ViewQuestionsSerializer
from meetups.models import Meetup
from utils.validators import valid_string
# Create your views here.


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
    """
    permission_classes = [permissions.IsAuthenticated]

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
