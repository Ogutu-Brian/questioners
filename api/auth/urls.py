from django.conf.urls import include
from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken
from .views import (SignUpView, ResendActivationView, ActivationView,
                    LoginView, LogoutView, ChangePasswordView, ChangeEmailView,
                    PasswordResetView, PasswordResetConfirmView, SocialAuthView,
                    SocialSigUpView)


urlpatterns = [     
     path('signup/', SignUpView.as_view(), name='user_signup'),
     path('resend/', ResendActivationView.as_view(), name='user_resend'),
     path('activate/', ActivationView.as_view(), name='user_activate'),
     path('login/', ObtainJSONWebToken.as_view(), name='user_login'),
     path('logout/', LogoutView.as_view(), name='user_logout'),
     path('change_password/', ChangePasswordView.as_view(),
          name='change_password'),
     path('change_email/', ChangeEmailView.as_view(), name='change_email'),
     path('reset_password/', PasswordResetView.as_view(),
          name='reset_password'),
     path('reset_password_confirm/', PasswordResetConfirmView.as_view(),
          name='reset_password_confirm'),
     path('google_oauth2/', SocialAuthView.as_view(), name='social'),
     path('social/signup', SocialSigUpView.as_view(), name='social_signup')
]
