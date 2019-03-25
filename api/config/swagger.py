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
                    url='/api/auth/google/signup',
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
                    url='/api/auth/google/login',
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
                'confirm rest': coreapi.Link(
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
                            type='array',
                            location='form',
                            description='Descriptive tags of the meetup'
                        ),
                        coreapi.Field(
                            name='images',
                            type='array',
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
                    fields=[
                        coreapi.Field(
                            name='page_limit',
                            required=False,
                            location='query',
                        ),
                        coreapi.Field(
                            name='page',
                            required=False,
                            location='query'
                        )
                    ],
                    description='View all meetups'
                ),
                'specific meetup': coreapi.Link(
                    url='/api/meetups/{meetupId}',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path'
                        )
                    ],
                    description='View specific meetup'
                ),
                'upcoming meetups': coreapi.Link(
                    url='/api/meetups/upcoming/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='page_limit',
                            required=False,
                            location='query',
                        ),
                        coreapi.Field(
                            name='page',
                            required=False,
                            location='query'
                        )
                    ],
                    description='View upcoming meetups'
                ),
                'Rsvp meetup': coreapi.Link(
                    url='/api/{meetupId}/rsvp',
                    action='POST',
                    description='Rsvp a specific meetup',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path',
                            description='Specific Meetup id'
                        ),

                        coreapi.Field(
                            name='response',
                            required=True,
                            location='form',
                            description='Response is either Yes, No or Maybe'
                        )
                    ]
                ),
                'Delete meetups': coreapi.Link(
                    url='/api/meetups/{meetupId}/',
                    action='DELETE',
                    description='Delete a specific meetup',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path'
                        )
                    ]
                ),
                'Update Meetup': coreapi.Link(
                    url='/api/meetups/{meetupId}/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path',
                            description='The meetup id'
                        ),
                        coreapi.Field(
                            name='title',
                            required=False,
                            location='form',
                            description='A title for the meetup'
                        ),
                        coreapi.Field(
                            name='body',
                            required=False,
                            location='form',
                            description='The body of the meetup'
                        ),
                        coreapi.Field(
                            name='location',
                            required=False,
                            location='form',
                            description='Where the meetup will be held'
                        ),
                        coreapi.Field(
                            name='scheduled_date',
                            required=False,
                            location='form',
                            description='When the meetup will be held. Must be valid date and time'
                        ),
                        coreapi.Field(
                            name='tags',
                            required=False,
                            location='form',
                            type='array',
                            description='Meetup tags'
                        ),
                        coreapi.Field(
                            name='images',
                            required=False,
                            location='form',
                            type='array',
                            description='Meetup image urls'
                        )
                    ],
                    description='Updating a meetup'
                )
            },
            'Questions': {
                'Post question': coreapi.Link(
                    # fetch meetup id from the database
                    url='/api/meetups/{meetupId}/questions/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path',
                            description='Id of the specific meetup id'
                        ),
                        coreapi.Field(
                            name='title',
                            required=True,
                            location='form',
                            description='The title of the question being asked'
                        ),
                        coreapi.Field(
                            name='body',
                            required=True,
                            location='form',
                            description='The description of the question beng asked'
                        )
                    ],
                    description='Posting a question to a specific meetup endpoint'
                ),
                'view question on meetups': coreapi.Link(
                    url='/api/meetups/{meetupId}/questions',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path',
                            description='Id of the meetup'
                        ),
                        coreapi.Field(
                            name='page',
                            required=False,
                            location='query',
                            description='page number'
                        ),
                        coreapi.Field(
                            name='page_limit',
                            required=False,
                            location='query',
                            description='The limit of data displayed per page'
                        ),
                    ],
                    description='Fetching questions on a specific meetup'
                ),
                'Delete questions': coreapi.Link(
                    url='/api/meetups/{meetupid}/questions/{questionid}/',
                    action='DELETE',
                    description='Delete a specific question',
                    fields=[
                        coreapi.Field(
                            name='meetupid',
                            required=True,
                            location='path'
                        ),
                        coreapi.Field(
                            name='questionid',
                            required=True,
                            location='path'
                        )
                    ],
                ),
                'Upvote a question': coreapi.Link(
                    url='/api/meetups/{meetupId}/questions/{questionId}/upvote',
                    action='PATCH',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path',
                            description='Id of the meetup from which the question is got'
                        ),
                        coreapi.Field(
                            name='questionId',
                            required=True,
                            location='path',
                            description='Id of the question to be upvoted'
                        )
                    ],
                    description='Upvoting a specific question'
                ),
                'Downvote a question': coreapi.Link(
                    url='/api/meetups/{meetupId}/questions/{questionId}/downvote',
                    action='PATCH',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path',
                            description='Id of the meetup from which the question is got'
                        ),
                        coreapi.Field(
                            name='questionId',
                            required=True,
                            location='path',
                            description='Id of the question to be downvoted'
                        )
                    ],
                    description='Downvoting a specific question'
                ),
                'view question on meetups': coreapi.Link(
                    url='/api/meetups/{meetupId}/questions',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path',
                            description='Id of the meetup'
                        ),
                        coreapi.Field(
                            name='page',
                            required=False,
                            location='query',
                            description='page number'
                        ),
                        coreapi.Field(
                            name='page_limit',
                            required=False,
                            location='query',
                            description='The limit of data displayed per page'
                        ),
                    ],
                    description='Fetching questions on a specific meetup'
                ),
                'Update existing questions': coreapi.Link(
                    # fetch meetup id from the database
                    url='/api/meetups/{meetupId}/questions/{questionId}/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path',
                            description='Id of the specific meetup id'
                        ),
                        coreapi.Field(
                            name='questionId',
                            required=True,
                            location='path',
                            description='Id of the specific question id'
                        ),
                        coreapi.Field(
                            name='title',
                            required=True,
                            location='form',
                            description='The title of the question being updated'
                        ),
                        coreapi.Field(
                            name='body',
                            required=True,
                            location='form',
                            description='A new description of the'
                        )
                    ],
                    description='Update an existing question'
                ),
            },
            'Answers': {
                'new answer': coreapi.Link(
                    url='/api/meetups/{meetupId}/questions/{questionId}/answer/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path',
                            description='Id of the specific meetup id'
                        ),
                        coreapi.Field(
                            name='questionId',
                            required=True,
                            location='path',
                            description='Id of the specific question id'
                        ),
                        coreapi.Field(
                            name='body',
                            required=True,
                            location='form',
                            description='A description of the answer'
                        ),
                    ],
                    description='Create a new Answer'
                ),
                'Get all Answers': coreapi.Link(
                    url='/api/meetups/{meetupId}/questions/{questionId}/answers/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path'
                        ),                    
                        coreapi.Field(
                            name='questionId',
                            required=True,
                            location='path'
                        )
                    ],
                    description='get all existing answers'
                ),
                'update existing answer': coreapi.Link(
                    url='/api/meetups/{meetupId}/questions/{questionId}/answers/{answerId}',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path',
                            description='A specific meetup id of an existing meetup'
                        ),
                        coreapi.Field(
                            name='questionId',
                            required=True,
                            location='path',
                            description='A specific question id of an existing question'
                        ),
                        coreapi.Field(
                            name='answerId',
                            required=True,
                            location='path',
                            description='A specific answer id of an existing answer'
                        ),
                        coreapi.Field(
                            name='body',
                            required=True,
                            location='form',
                            description='A new description of the answer'
                        )
                    ],
                    description='Update an existing answer'
                ),
                'Delete answer': coreapi.Link(
                    url='/api/meetups/{meetupId}/questions/{questionId}/answers/{answerId}/',
                    action='DELETE',
                    description='Delete a specific answer',
                    fields=[
                        coreapi.Field(
                            name='meetupId',
                            required=True,
                            location='path',
                            description='A specific meetup id of an existing question' ),
                        coreapi.Field( 
                            name='questionId',
                            required=True, 
                            location='path',
                            description='A specific question id of an existing question' ),
                        coreapi.Field(
                            name='answerId',
                            required=True, 
                            location='path', 
                            description='A specific answer id of an existing answer' ) 
                       ]
                ),
            }

        }
    )
    return response.Response(schema)