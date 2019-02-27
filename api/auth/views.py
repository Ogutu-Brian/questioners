from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import PermissionDenied

from djoser import utils, signals
from djoser.compat import get_user_email, get_user_email_field_name
from djoser.conf import settings

from config import exceptions
from . import serializers
from . import mailer

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
    serializer_class = serializers.UidAndTokenSerializer
    permission_classes = [permissions.AllowAny]
    token_generator = default_token_generator

    def _action(self, serializer):
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
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = serializers.TokenSerializer
        return Response(data=token_serializer_class(token).data)


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def delete(request):
        utils.logout_user(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        return Response(status=status.HTTP_204_NO_CONTENT)

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
        return Response(status=status.HTTP_204_NO_CONTENT)
