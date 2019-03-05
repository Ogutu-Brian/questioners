"""
uril patterns for meetups
"""
from django.urls import path
from meetups.views import MeetupViews
urlpatterns = [
    path('meetups', MeetupViews.as_view())
]
