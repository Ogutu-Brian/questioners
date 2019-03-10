"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view

from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls.static import static

from auth.views import AuthApiListView
from utils.router import DefaultRouterWithAPIViews

from .swagger import schema_view_swagger 

admin.site.site_header = settings.ADMIN_SITE_HEADER

router = DefaultRouterWithAPIViews()
router.register('api/auth', AuthApiListView)

# schema_view_swagger = get_swagger_view(title='Questioner API')

schema_view = get_schema_view(title=settings.API_BROWSER_HEADER, public=True)
doc_urls = include_docs_urls(title=settings.API_BROWSER_HEADER)
api_browser_urls = include('rest_framework.urls')
auth_urls = include('auth.urls')
meetup_urls = include('meetups.urls')
oauth2_urls = include('rest_framework_social_oauth2.urls')

meetup_urls = include('meetups.urls')
<<<<<<< HEAD
oauth2_urls = include('rest_framework_social_oauth2.urls')

=======
>>>>>>> #164275603 Post Meetup Endpoint for Questioner (Backend) (#6)
urlpatterns = [
    path('auth/', oauth2_urls),
    path('api/', doc_urls),
    path('api/auth/', auth_urls),
    path('api/', meetup_urls),
    path('api/schema/', schema_view),
    path('api/schema/swagger/', schema_view_swagger),
    path('api/browser/', api_browser_urls),
    path('api/admin/', admin.site.urls),
    path('socialauth/', include('rest_framework_social_oauth2.urls')),
]

urlpatterns += router.urls

# Serve media assets for development, only works while DEBUG=True
# https://docs.djangoproject.com/en/2.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
