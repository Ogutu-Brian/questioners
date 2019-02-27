"""
uril patterns for answers
"""
from django.urls import path
from .views import AnswersPostView, UpdateAnswer

urlpatterns = [
    path('<str:meetupId>/questions/<str:id>/answer/', AnswersPostView.as_view(), name='post_answer'),
    path('<meetupId>/questions/<questionId>/answers/<answerId>', UpdateAnswer.as_view(), name='update_answer'),
]