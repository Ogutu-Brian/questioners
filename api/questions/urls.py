"""
Urls for questions Epic
"""

from django.urls import path
from questions.views import QuestionViews, ViewQuestionsView

urlpatterns = [         
     path('<str:id>/questions/', QuestionViews.as_view(), name='question'),
     path('<str:id>/questions', ViewQuestionsView.as_view(), name='view_questions'),
]
