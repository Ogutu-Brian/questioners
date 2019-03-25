"""
Urls for questions Epic
"""

from django.urls import path
from questions.views import (QuestionViews, ViewQuestionsView,
                             UpvoteQuestion, DownvoteQuestion, QuestionEditViews, ViewSpecificQuestionView)
urlpatterns = [
    path('<str:id>/questions/', QuestionViews.as_view(), name='question'),
    path('<str:id>/questions', ViewQuestionsView.as_view(), name='view_questions'),
    path('<str:meetup_id>/questions/<str:question_id>/upvote',
         UpvoteQuestion.as_view(), name='upvote_question'),
    path('<str:meetup_id>/questions/<str:question_id>/downvote',
         DownvoteQuestion.as_view(), name='downvote_question'),
    path('<str:m_id>/questions/<str:id>/',
         QuestionEditViews.as_view(), name='delete_question'),
    path('<str:m_id>/questions/<str:id>/',
         QuestionEditViews.as_view(), name='edit_question'),
    path('<str:m_id>/questions/<str:id>',
         ViewSpecificQuestionView.as_view(), name='specific_question'),
]
