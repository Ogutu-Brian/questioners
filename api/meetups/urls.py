"""
uril patterns for meetups
"""
from django.urls import path, re_path
from django.conf.urls import url
from meetups.views import (
    MeetupViews,
    GetAllMeetups,
    GetSpecificMeetup,
    GetUpcomingMeetups,
    RspvPostView,
    GetRsvps
)

urlpatterns = [
    path('meetups', MeetupViews.as_view()),
    path('meetups/', GetAllMeetups.as_view()),
    path('meetups/<str:meetupid>', GetSpecificMeetup.as_view()),
    path('meetups/upcoming/', GetUpcomingMeetups.as_view()),
    path('meetups/<str:id>/rsvp', RspvPostView.as_view(), name='rsvp'),
    path('meetups/<str:meetupid>/', MeetupViews.as_view()),
    path('meetups/<str:meetup_id>/rsvps', GetRsvps.as_view())
]
