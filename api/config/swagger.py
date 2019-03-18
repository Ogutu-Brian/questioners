from rest_framework_swagger.renderers import (SwaggerUIRenderer,
                                              OpenAPIRenderer)
from rest_framework.decorators import (renderer_classes, authentication_classes,
                                       api_view, permission_classes)
from rest_framework import response
from rest_framework.permissions import AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

import coreapi


@api_view()
@permission_classes((AllowAny, ))
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
@authentication_classes((JSONWebTokenAuthentication, ))
def schema_view_swagger(request):
    schema = coreapi.Document(
        title='Questioner API',
        url='https://questioners-two-staging.herokuapp.com/',  # replace with your url
        content={
            'Users': {
                'signup': coreapi.Link(
                    url='/api/auth/signup/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='name',
                            required=True,
                            location='form',
                            description='Name of the new user'
                        ),
                        coreapi.Field(
                            name='nick_name',
                            required=True,
                            location='form',
                            description='Nickname of the new user'
                        ),
                        coreapi.Field(
                            name='email',
                            required=True,
                            location='form',
                            description='Email of the user'
                        ),
                        coreapi.Field(
                            name='password',
                            required=True,
                            location='form',
                            description='A password for the user'
                        )
                    ],
                    description='Using basic authentication to signup'
                ),
                'activate': coreapi.Link(
                    url='/api/auth/activate/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='uid',
                            required=True,
                            location='form',
                            description='The hashed user id'
                        ),
                        coreapi.Field(
                            name='token',
                            required=True,
                            location='form',
                            description='The activation token'
                        )
                    ],
                    description='Account activation using email'
                ),
                'resend activation': coreapi.Link(
                    url='/api/auth/resend/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='email',
                            required=True,
                            location='form',
                            description='The user email to activate'
                        )
                    ],
                    description='Resend account activation email'
                ),
                'social signup': coreapi.Link(
                    url='/api/auth/social/signup',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='id_token',
                            required=True,
                            location='form',
                            description='Id token acquired from google provider'
                        )
                    ],
                    description='Using google authentication to signup'
                ),
                'login': coreapi.Link(
                    url='/api/auth/login/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='email',
                            required=True,
                            location='form',
                            description='An existing email used during signup'
                        ),
                        coreapi.Field(
                            name='password',
                            required=True,
                            location='form',
                            description='A password used during signup'
                        )
                    ],
                    description='Using basic authentication to login'
                ),
                'google auth': coreapi.Link(
                    url='/api/auth/google_oauth2/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='id_token',
                            required=True,
                            location='form',
                            description='Id token acquired from google provider'
                        )
                    ],
                    description='Using google authentication to login'
                ),
                'reset password': coreapi.Link(
                    url='/api/auth/reset_password/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='email',
                            required=True,
                            location='form',
                            description='Email used for registration required'
                        )
                    ],
                    description='Request reset password'
                ),
                'confirm reset': coreapi.Link(
                    url='/api/auth/reset_password_confirm/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='uid',
                            required=True,
                            location='form',
                            description='User ID from the confirmation email'
                        ),
                        coreapi.Field(
                            name='token',
                            required=True,
                            location='form',
                            description='Tokens from the confirmation email'
                        ),
                        coreapi.Field(
                            name='new_password',
                            required=True,
                            location='form',
                            description='New_password'
                        ),
                        coreapi.Field(
                            name='re_new_password',
                            required=True,
                            location='form',
                            description='Re enter new password'
                        )
                    ],
                    description='Reset password'
                ),
                'change password': coreapi.Link(
                    url='/api/auth/change_password/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='new_password',
                            required=True,
                            location='form',
                            description='New password'
                        ),
                        coreapi.Field(
                            name='re_new_password',
                            required=True,
                            location='form',
                            description='Re-enter new password'
                        ),
                        coreapi.Field(
                            name='current_password',
                            required=True,
                            location='form',
                            description='Old password'
                        )
                    ],
                    description='Change password'
                ),
                'logout': coreapi.Link(
                    url='/api/auth/logout/',
                    action='DELETE',
                    description='User Logout'
                )
            },
            'Meetups': {
                'new meetup': coreapi.Link(
                    url='/api/meetups',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='title',
                            required=True,
                            location='form',
                            description='The title of the meetup'
                        ),
                        coreapi.Field(
                            name='body',
                            required=True,
                            location='form',
                            description='A description of the meetup topic'
                        ),
                        coreapi.Field(
                            name='location',
                            required=True,
                            location='form',
                            description='The venue of the meetup'
                        ),
                        coreapi.Field(
                            name='scheduled_date',
                            required=True,
                            location='form',
                            description='The date and time of the meetup'
                        ),
                        coreapi.Field(
                            name='tags',
                            required=False,
                            location='form',
                            description='Descriptive tags of the meetup'
                        ),
                        coreapi.Field(
                            name='images',
                            required=False,
                            location='form',
                            description='Image URLs for the meetup'
                        )
                    ],
                    description='Create a new Meetup'
                ),
                'all meetups': coreapi.Link(
                    url='/api/meetups/',
                    action='GET',
                    description='View all meetups'
                ),
                'specific meetup': coreapi.Link(
                    url='/api/meetups/{meetupid}',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='meetupid',
                            required=True,
                            location='path'
                        )
                    ],
                    description='View specific meetup'
                ),
                'upcoming meetups': coreapi.Link(
                    url='/api/meetups/upcoming/',
                    action='GET',
                    description='View upcoming meetups'
                )
            },
            'Meetups':{
                'update': coreapi.Link(
                    url= '/api/update/{id}',
                    action= 'PUT',
                    fields= [
                        coreapi.Field(
                            name = 'id',
                            required = True,
                            location = 'path',
                            description = 'The meetup id'
                        ),
                        coreapi.Field(
                            name = 'title',
                            required = False,
                            location = 'form',
                            description = 'A title for the meetup'
                        ),
                        coreapi.Field(
                            name = 'body',
                            required = False,
                            location = 'form',
                            description = 'The body of the meetup'
                        ),
                        coreapi.Field(
                            name = 'location',
                            required = False,
                            location = 'form',
                            description = 'Where the meetup will be held'
                        ),
                        coreapi.Field(
                            name = 'scheduled_date',
                            required = False,
                            location = 'form',
                            description = 'When the meetup will be held. Must be valid date and time'
                        ),
                        coreapi.Field(
                            name = 'tags',
                            required = False,
                            location = 'form',
                            description = 'Meetup tags'
                        ),
                        coreapi.Field(
                            name = 'images',
                            required = False,
                            location = 'form',
                            description = 'Meetup image urls'
                        )
                    ],
                    description = 'Updating a meetup'   
                )
            }
        }
    )
    return response.Response(schema)
