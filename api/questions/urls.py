"""
Urls for questions Epic
"""

from django.urls import path
from questions.views import QuestionViews

urlpatterns = [     
     path('<str:id>/question/', QuestionViews.as_view(), name='question'),
]
