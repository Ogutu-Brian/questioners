"""
uril patterns for meetups
"""
from django.urls import path
from meetups.views import (
    MeetupViews,
    GetAllMeetups,
    GetSpecificMeetup,
    GetUpcomingMeetups,
    UpdateMeetup,
    RsvpView, RspvPostView
)

urlpatterns = [
    path('meetups', MeetupViews.as_view()),
    path('meetups/', GetAllMeetups.as_view()),
    path('meetups/<str:meetupid>', GetSpecificMeetup.as_view()),
    path('meetups/upcoming/', GetUpcomingMeetups.as_view()),
    path('update/<id>', UpdateMeetup.as_view()),
    path('response', RsvpView.as_view()),
    path('<str:id>/rsvp', RspvPostView.as_view(), name='rsvp')
]
