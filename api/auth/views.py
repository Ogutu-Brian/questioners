import jwt
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend
from rest_framework_jwt.settings import api_settings
from djoser import utils, signals
from djoser.compat import get_user_email, get_user_email_field_name
from djoser.conf import settings

from config import settings as sett

from google.oauth2 import id_token
from google.auth.transport import requests

from users.models import User, TokenBlacklist

from config import exceptions
from . import serializers
from . import mailer

from google.oauth2 import id_token
from google.auth.transport import requests

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class AuthApiListView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def aggregate_urlpattern_names():
        from . import urls
        urlpattern_names = [pattern.name for pattern in urls.urlpatterns]

        return urlpattern_names

    @staticmethod
    def get_urls_map(request, urlpattern_names, fmt):
        urls_map = {}
        for urlpattern_name in urlpattern_names:
            try:
                url = reverse(urlpattern_name, request=request, format=fmt)
            except NoReverseMatch:
                url = ''
            urls_map[urlpattern_name] = url
        return urls_map

    def get(self, request, fmt=None):
        urlpattern_names = self.aggregate_urlpattern_names()
        urls_map = self.get_urls_map(request, urlpattern_names, fmt)
        return Response(urls_map)


class SignUpView(generics.CreateAPIView):
    serializer_class = serializers.SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        signals.user_registered.send(sender=self.__class__, user=user,
                                     request=self.request)

        context = {'user': user}
        recipient = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            mailer.ActivationEmail(self.request, context, recipient).send()
        elif settings.SEND_CONFIRMATION_EMAIL:
            mailer.ConfirmationEmail(self.request, context, recipient).send()


class SocialSigUpView(APIView):
    """
    A signup endpoint using google auth
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.SocialAuthSerializer

    def post(self, request):
        """
        User sign up with Google
        """
        not_active = True
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data.get("id_token")
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), '407408718192.apps.googleusercontent.com')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer')

            user, created = User.objects.update_or_create(
                email=idinfo.get('email'),
                defaults={
                    'name': idinfo.get('name'),
                    'nick_name': idinfo.get('given_name'),
                }
            )
            if(created):
                user.is_active = False
                user.save()
            else:
                if(user.is_active):
                    not_active = False
            if(not_active):
                created_user = User.objects.get(email=idinfo.get('email'))
                signals.user_registered.send(sender=self.__class__, user=user,
                                             request=self.request)
                context = {'user': user}
                recipient = [get_user_email(user)]
                if settings.SEND_ACTIVATION_EMAIL:
                    mailer.ActivationEmail(
                        self.request, context, recipient).send()
                elif settings.SEND_CONFIRMATION_EMAIL:
                    mailer.ConfirmationEmail(
                        self.request, context, recipient).send()
                response = {
                    "message": "A verification mail has been sent to you, please check your mail"
                }, status.HTTP_201_CREATED
            else:
                response = {
                    "error": "This account had been activated"
                }, status.HTTP_400_BAD_REQUEST
            return Response(response[0], response[1])
        except ValueError as e:
            return Response(
                {'error': str(e)}, status.HTTP_400_BAD_REQUEST
            )


class ResendActivationView(utils.ActionViewMixin, generics.GenericAPIView):
    serializer_class = serializers.EmailAccountSerializer
    permission_classes = [permissions.AllowAny]

    _users = None

    def _action(self, serializer):
        for user in self.get_users(serializer.data['email']):
            if user.is_active:
                raise exceptions.AlreadyProcessed(
                    _('The user account is already active.'))

            self.send_activation_email(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get_users(self, email):
        if self._users is None:
            email_field_name = get_user_email_field_name(User)
            self._users = User.objects.filter(
                **{email_field_name + '__iexact': email})
        return self._users

    def send_activation_email(self, user):
        context = {'user': user}
        recipient = [get_user_email(user)]
        mailer.ActivationEmail(self.request, context, recipient).send()


class ActivationView(utils.ActionViewMixin, generics.GenericAPIView):
    serializer_class = serializers.UidAndTokenQueryParamsSerializer
    permission_classes = [permissions.AllowAny]
    token_generator = default_token_generator

    def post(self):
        serializer = self.serializer_class
        user = serializer.user
        if user.is_active:
            raise exceptions.AlreadyProcessed(
                _('The user account is already active.'))

        user.is_active = True
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request)

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {'user': user}
            recipient = [get_user_email(user)]
            mailer.ConfirmationEmail(self.request, context, recipient).send()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(utils.ActionViewMixin, generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [permissions.AllowAny]

    def _action(self, serializer):
        login(self.request, serializer.user)
        token = jwt_encode_handler(
            jwt_payload_handler(serializer.user))
        resp = {
            'Message': 'Welcome {}. You are now logged in'.format(serializer.user),
            'token': token
        }
        return Response(data=resp, status=status.HTTP_200_OK)


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        auth = get_authorization_header(request).split()
        token = auth[1]
        TokenBlacklist.objects.update_or_create(token=token)
        return Response(data={'Message': 'You have been logged out'}, status=status.HTTP_200_OK)


class ChangeEmailView(utils.ActionViewMixin, generics.GenericAPIView):
    serializer_class = serializers.ChangeEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _action(self, serializer):
        user = self.request.user
        user_serializer = self.get_serializer(user, serializer.data)

        if user_serializer.is_valid():
            user_serializer.save()
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                context = {'user': user}
                recipient = [get_user_email(user)]
                mailer.ActivationEmail(self.request, context, recipient).send()

            utils.logout_user(self.request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(user_serializer.errors, status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(utils.ActionViewMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if settings.SET_PASSWORD_RETYPE:
            return serializers.ChangePasswordRetypeSerializer
        return serializers.ChangePasswordSerializer

    def _action(self, serializer):
        self.request.user.set_password(serializer.data['new_password'])
        self.request.user.save()

        if settings.LOGOUT_ON_PASSWORD_CHANGE:
            utils.logout_user(self.request)

        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetView(utils.ActionViewMixin, generics.GenericAPIView):
    serializer_class = serializers.EmailAccountSerializer
    permission_classes = [permissions.AllowAny]

    _users = None

    def _action(self, serializer):
        for user in self.get_users(serializer.data['email']):
            self.send_password_reset_email(user)
        return Response({"message": "reset link sent to your mail"}, status=status.HTTP_200_OK)

    def get_users(self, email):
        if self._users is None:
            email_field_name = get_user_email_field_name(User)
            users = User.objects.filter(
                **{email_field_name + '__iexact': email})
            self._users = [
                u for u in users if u.is_active and u.has_usable_password()
            ]
        return self._users

    def send_password_reset_email(self, user):
        context = {'user': user}
        recipient = [get_user_email(user)]
        mailer.PasswordResetEmail(self.request, context, recipient).send()


class PasswordResetConfirmView(utils.ActionViewMixin, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    token_generator = default_token_generator

    def get_serializer_class(self):
        if settings.PASSWORD_RESET_CONFIRM_RETYPE:
            return serializers.PasswordResetConfirmRetypeSerializer
        return serializers.PasswordResetConfirmSerializer

    def _action(self, serializer):
        serializer.user.set_password(serializer.data['new_password'])
        serializer.user.save()
        if self.request.user.is_authenticated:
            utils.logout_user(self.request)
        return Response({"message": "password successfully reset"}, status=status.HTTP_200_OK)


class SocialAuthView(generics.CreateAPIView):
    """Login via Google"""
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.SocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data.get("id_token")
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), '407408718192.apps.googleusercontent.com')
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer')
        except:
            data = {'Message': 'The token provided is invalid'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if idinfo:
            email = idinfo.get('email')
            name = idinfo.get('name')

        try:
            if User.objects.get(email=email):
                if User.objects.get(email=email).is_active:

                    data = {
                        "Message": "You are logged in.",
                        "email": email,
                        "name": name,
                        "token": jwt_encode_handler(
                            jwt_payload_handler(User.objects.get(email=email)))
                    }
                    return Response(data, status=status.HTTP_200_OK)
                data = {'Message': 'Activate your account to log in'}
                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        except:
            data = {'Message': 'No user with the given credentials found'}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
