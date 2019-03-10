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
        title = 'Questioner API',
        url = 'http://0.0.0.0:3000/', # replace with your url
        content = {
            'Users': {
                'login': coreapi.Link(
                    url = '/api/auth/login/',
                    action = 'POST',
                    fields = [
                        coreapi.Field(
                            name = 'email',
                            required = True,
                            location = 'form',
                            description = 'An existing email used during signup'
                        ),
                        coreapi.Field(
                            name = 'password',
                            required = True,
                            location = 'form',
                            description = 'A password used during signup'
                        )
                    ],
                    description = 'Using basic authentication to login'
                ),
                'google auth': coreapi.Link(
                    url = '/api/auth/google_oauth2/',
                    action = 'POST',
                    fields = [
                        coreapi.Field(
                            name = 'provider',
                            required = True,
                            location = 'form',
                            description = 'The name of google provider'
                        ),
                        coreapi.Field(
                            name = 'access_token',
                            required = True,
                            location = 'form',
                            description = 'Access token acquired from google provider'
                        )
                    ],
                    description = 'Using google authentication to login'
                )
            }
        }
    )
    return response.Response(schema)