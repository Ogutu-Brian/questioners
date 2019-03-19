"""
Views for operations performed on meetups
"""
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from django.db.utils import DataError

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render
from rest_framework.views import APIView, Response
from .models import Meetup, Tag, Image
from .serializers import (
    MeetupSerializer,
    TagSerializer,
    UpdateMeetupSerializer,
    FetchMeetupSerializer,
    RsvpSerializer
)
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils.validators import valid_string, valid_url, valid_meetup
from rest_framework.request import Request
from .models import Meetup, Tag, Image, Rsvp
from typing import Tuple
from rest_framework.decorators import permission_classes, api_view
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone

class MeetupViews(APIView):
    """
    Views for meetup endpoints
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Post Endpoint for creating meetup
        POST /api/auth/meetups
        """
        is_valid_meetup, errors = valid_meetup(request)
        if is_valid_meetup:
            request.data['creator'] = request.user
            tags = request.data.get('tags')
            images = request.data.get('images')
            tag_list = []
            image_list = []
            if tags:
                for tag in tags:
                    tag_object, created = Tag.objects.update_or_create(
                        tag_name=tag,
                        defaults={
                            'tag_name': tag
                        }
                    )
                    tag_list.append(tag_object)
            if images:
                for image in images:
                    image_object, created = Image.objects.update_or_create(
                        image_url=image,
                        defaults={
                            'image_url': image
                        }
                    )
                    image_list.append(image_object)
            data = request.data
            serializer = MeetupSerializer(data=data)
            if not (request.user.is_staff):
                context = {
                    'error': 'Admin only can create meetup'
                }
                response = Response(
                    context,
                    status.HTTP_401_UNAUTHORIZED
                )
            elif serializer.is_valid():
                data = request.data
                meetup, created = Meetup.objects.update_or_create(
                    title=data.get('title'),
                    location=data.get('location'),
                    scheduled_date=data.get('scheduled_date'),
                    defaults={
                        'body': data.get('body'),
                        'creator': data.get('creator')
                    }
                )
                for image_object in image_list:
                    meetup.image_url.add(image_object)
                for tag_item in tag_list:
                    meetup.tags.add(tag_item)
                response = Response({
                    'data': serializer.data,
                    'status': status.HTTP_201_CREATED
                },
                    status=status.HTTP_201_CREATED
                )
            else:
                response = Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            response = Response(
                data=errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return response

    def delete(self, request, meetupid, format=None) -> Response:
        """
        Endpoint to deleting specific meetup
        Delete /api/meetups/<meetupId>/
        """
        response = {}

        try:
            meetup = Meetup.objects.get(id=meetupid)
            meetup.delete()
            response = {
                "message": "succefully deleted",
                "status": status.HTTP_204_NO_CONTENT
            }
        except (ObjectDoesNotExist, ValidationError) as e:
            response = {
                'error': str(e),
                'status': status.HTTP_404_NOT_FOUND,
            }

        return Response(
            data=response,
            status=response.get('status')
        )


class GetAllMeetups(APIView):
    """
    Class view for requesting all meetups
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request) -> Response:
        """
        A GET endpoint for getting all meetups in the database
        GET /api/meetups/
        """
        page_limit = request.GET.get('page_limit')
        if not page_limit or not page_limit.isdigit():
            page_limit = 10
        meetups = Meetup.objects.all()
        response = None
        if not meetups:
            response = Response({
                "error": "There are no meetups",
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            paginator = PageNumberPagination()
            paginator.page_size = page_limit
            result_page = paginator.paginate_queryset(meetups, request)
            serializer = FetchMeetupSerializer(result_page, many=True)
            response = paginator.get_paginated_response(serializer.data)
        return response


class GetSpecificMeetup(APIView):
    """
    Class for handling get of specific meetups
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request, meetupid: str) -> Response:
        """
        A GET endpoint for getting specific meetup
        GET /api/meetups/<meetupId>
        """
        response = {}
        try:
            meetup = Meetup.objects.get(id=meetupid)
            serializer = FetchMeetupSerializer(meetup)
            response = {
                "data": [serializer.data],
                "status": status.HTTP_200_OK
            }
        except:
            response = {
                'error': 'A meetup with that id does not exist',
                'status': status.HTTP_404_NOT_FOUND
            }
        return Response(
            data=response,
            status=response.get('status')
        )


class GetUpcomingMeetups(APIView):
    """
    Class for handling the get of upcoming meetups
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request) -> Response:
        """
        Gets upcoming meetups
        GET /api/meetups/upcoming/
        """
        page_limit = request.GET.get('page_limit')
        if not page_limit or not page_limit.isdigit():
            page_limit = 10
        upcoming_meetups = Meetup.objects.filter(
            scheduled_date__gte=timezone.now())
        if upcoming_meetups:
            paginator = PageNumberPagination()
            paginator.page_size = page_limit
            result_page = paginator.paginate_queryset(
                upcoming_meetups, request)
            serializer = FetchMeetupSerializer(result_page, many=True)
            response = paginator.get_paginated_response(serializer.data)
        else:
            response = Response(
                data={
                    'error': 'There are no upcoming meetups',
                    'status': status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return response


class UpdateMeetup(APIView):
    """
    Class for updating meetups endpoint
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_classes = UpdateMeetupSerializer

    def put(self, request: Request, id: str) -> Response:

        is_valid_meetup, errors = valid_meetup(request)
        meetup = None
        try:
            meetup = Meetup.objects.get(id=id)
        except:
            errors.append({
                'Error': 'The specified meetup does not exist'
            })

            is_valid_meetup = False

        if is_valid_meetup:
            request.data['creator'] = request.user
            tags = request.data.get('tags')
            images = request.data.get('images')
            tag_list = []
            image_list = []
            if tags:
                meetup.tags.clear()
                for tag in tags:
                    tag_object, created = Tag.objects.update_or_create(
                        tag_name=tag,
                        defaults={
                            'tag_name': tag
                        }
                    )
                    tag_list.append(tag_object)
            if images:
                meetup.image_url.clear()
                for image in images:
                    image_object, created = Image.objects.update_or_create(
                        image_url=image,
                        defaults={
                            'image_url': image
                        }
                    )
                    image_list.append(image_object)
            data = request.data
            if not(request.user.is_staff):
                context = {
                    'Error': 'Only an admin user can update a meetup'
                }
                response = Response(
                    context, status.HTTP_401_UNAUTHORIZED
                )
            else:
                data = request.data
                qs = Meetup.objects.filter(title=data.get('title'))
                if data.get('title'):
                    qs = qs.exclude(pk=meetup.id)
                    if qs.exists():
                        return Response(
                            data={
                                'Error': 'That title is already taken'
                            },
                            status=status.HTTP_406_NOT_ACCEPTABLE
                        )
                    meetup.title = data.get('title')
                if data.get('location'):
                    meetup.location = data.get('location')
                if data.get('scheduled_date'):
                    meetup.scheduled_date = data.get('scheduled_date')
                if data.get('body'):
                    meetup.body = data.get('body')
                for image_object in image_list:
                    meetup.image_url.add(image_object)
                for tag_item in tag_list:
                    meetup.tags.add(tag_item)

                meetup.save()
                serializer = UpdateMeetupSerializer(meetup)
                context = {
                    'data': [serializer.data],
                }
                response = Response(
                    data=context,
                    status=status.HTTP_201_CREATED
                )
        else:
            response = Response(
                data=errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return response


class RsvpView(APIView):
    """
    We can see all the response from users
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get all available RSVP
        """
        response = Rsvp.objects.all()
        serializer = RsvpSerializer(response, many=True)
        return Response(
            {"rsvp": serializer.data}
        )


class RspvPostView(APIView):
    """
    User can post an Rsvp
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        """
        Create an RSVP
        """
        try:
            queryset = Meetup.objects.all()
            request.data['responder'] = request.user
            serializer = RsvpSerializer(data=request.data)
            # import pdb
            # pdb.set_trace()

            if serializer.is_valid():
                Rsvp.objects.update_or_create(

                    meetup=get_object_or_404(queryset, id=id),
                    responder=request.data.get('responder'),
                    defaults={
                        'response': request.data.get('response'),
                        'meetup': get_object_or_404(queryset, id=id),
                        'responder': request.data.get('responder')
                    }
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ValidationError, DataError) as e:
            return Response({
                "error": "No meetup found"
            }, status=status.HTTP_404_NOT_FOUND)
