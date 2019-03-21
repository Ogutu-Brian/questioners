"""
Urls for questions Epic
"""

from django.urls import path
from questions.views import QuestionViews, ViewQuestionsView, QuestionEditViews

urlpatterns = [         
     path('<str:id>/questions/', QuestionViews.as_view(), name='question'),
     path('<str:id>/questions', ViewQuestionsView.as_view(), name='view_questions'),
     path('<str:m_id>/questions/<str:id>/', QuestionEditViews.as_view(), name='delete_question'),
]
