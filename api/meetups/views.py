"""
Views for operations performed on meetups
"""
from django.shortcuts import render
from rest_framework.views import APIView, Response
from .models import Meetup, Tag, Image
from .serializers import MeetupSerializer, TagSerializer
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from utils.validators import valid_string, valid_url
from rest_framework.request import Request
from typing import Tuple


def valid_meetup(request) -> Tuple:
    """
    Validates meeetup data that is not handled by django
    """
    data = request.data
    errors = []
    is_valid = True
    if data.get('title') and not valid_string(data.get('title')):
        errors.append({
            'error': '{} is not a valid meetup title'.format(data.get('title'))
        })
        is_valid = False
    elif data.get('body') and not valid_string(data.get('body')):
        errors.append({
            'error': '{} is not a valid meetup body'.format(data.get('body'))
        })
        is_valid = False
    elif data.get('location') and not valid_string(data.get('location')):
        errors.append({
            'error': '{} is not a valid meetup location'.format(data.get('location'))
        })
        is_valid = False
    if data.get('images'):
        for image in data.get('images'):
            if not valid_url(image):
                is_valid = False
                errors.append({
                    'error': '{} is not a valid image url'.format(image)
                })
                break
    return is_valid, errors


class MeetupViews(APIView):
    """
    Views for meetup endpoints
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Post Endpoint for creating meetup
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
            if(tag_list):
                data['tags'] = tag_list
            if(image_list):
                data['image_url'] = image_list
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
                Meetup.objects.update_or_create(
                    title=data.get('title'),
                    location=data.get('location'),
                    scheduled_date=data.get('scheduled_date'),
                    defaults={
                        'body': data.get('body'),
                        'creator': data.get('creator')
                    }
                )
                response = Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                response = Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            response = Response(
                errors,
                status.HTTP_400_BAD_REQUEST
            )
        return response
