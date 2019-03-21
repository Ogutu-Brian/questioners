"""
A collection of validators used for Questioner application
"""
from validator_collection import checkers
import re
from rest_framework.request import Request
from typing import Tuple

def valid_string(input_string: str) -> bool:
    """
    Checks if the input string contains valid characters for fields
    and does not begin with whitespaces
    """
    regex = '[a-zA-Z0-9]'
    is_valid = True
    if not re.match(regex, input_string.strip()):
        is_valid = False
    return is_valid


def valid_url(input_url: str) -> bool:
    """
    checks if the input url is valid
    """
    return checkers.is_url(input_url)


def valid_meetup(request: Request) -> Tuple:
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


def valid_question(request: Request) -> Tuple:
    """
    Validates questions data that is not handled by django
    """
    data = request.data
    errors = []
    is_valid = True
    if data.get('title') and not valid_string(data.get('title')):
        errors.append({
            'error': '{} is not a valid question title'.format(data.get('title'))
        })
        is_valid = False
    elif data.get('body') and not valid_string(data.get('body')):
        errors.append({
            'error': '{} is not a valid question body'.format(data.get('body'))
        })
        is_valid = False
    return is_valid, errors