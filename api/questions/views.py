from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework import permissions, status
from rest_framework.views import APIView, Response
from rest_framework.pagination import PageNumberPagination

from questions.models import Question
from questions.serializers import QuestionsSerializer, ViewQuestionsSerializer
from meetups.models import Meetup
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
                Question.objects.update_or_create(
                    title=request.data.get('title'),
                    body=request.data.get('body'),
                    defaults={
                        'meetup': get_object_or_404(queryset, id=id),
                        'created_by': request.data.get('created_by')
                    }
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            message = str(e)
            return Response({
                "error": message
            }, status=status.HTTP_404_NOT_FOUND)

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
            pagination_class = PageNumberPagination()
            pagination_class.page_size = 5
            page = pagination_class.paginate_queryset(questions, request)
            serializer = ViewQuestionsSerializer(page, many=True)
            paginated_response = pagination_class.get_paginated_response(
                serializer.data)
            return paginated_response
        return Response({
            "error": "There are no questions"
        }, status=status.HTTP_404_NOT_FOUND)
