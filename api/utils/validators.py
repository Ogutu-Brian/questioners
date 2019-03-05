"""
A collection of validators used for Questioner application
"""
from validator_collection import checkers
import re


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
