"""
url patterns for answers
"""
from django.urls import path
from .views import AnswersPostView, UpdateAnswer, GetAnswerView, DeleteAnswer, UpvoteAnswer, DownvoteAnswer


urlpatterns = [
    path('<str:meetupId>/questions/<str:questionId>/answers/', AnswersPostView.as_view(), name='post_answer'),
    path('<meetupId>/questions/<questionId>/answers/<answerId>', UpdateAnswer.as_view(), name='update_answer'),
    path('<str:meetupId>/questions/<str:questionId>/answers', GetAnswerView.as_view(), name='Get_all_answers'),
    path('<str:meetupId>/questions/<str:questionId>/answers/<str:answerId>/', DeleteAnswer.as_view(), name='delete_answer'),
    path('<str:meetupId>/questions/<str:questionId>/answers/<str:answerId>/upvote', UpvoteAnswer.as_view(), name='upvote_answer'),
    path('<str:meetupId>/questions/<str:questionId>/answers/<str:answerId>/downvote', DownvoteAnswer.as_view(), name='downvote_answer')
]
