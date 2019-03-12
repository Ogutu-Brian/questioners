from rest_framework_swagger.renderers import SwaggerUIRenderer,  OpenAPIRenderer
from rest_framework.decorators import renderer_classes, api_view, permission_classes
from rest_framework import response
from rest_framework.permissions import AllowAny

import coreapi


@api_view()
@permission_classes((AllowAny, ))
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view_swagger(request):
    schema = coreapi.Document(
        title='Questioner API',
        url='http://127.0.0.1:8000/',  # replace with your url
        content={
            'Users': {
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
                    description='No authentication required'
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
                    description='No authentication required'
                )
            }
        }
    )
    return response.Response(schema)
