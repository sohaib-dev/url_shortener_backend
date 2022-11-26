"""
    It contains the url validation methods.
"""

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

SUPPORTED_SCHEMES = []


def check_scheme(_scheme: str, _schemes_list=[]) -> bool:
    """ It checks whether the scheme provided is supported by the system or not.

    :param _schemes_list:
    :param _scheme: _scheme
    :return: bool
    """

    if _scheme in _schemes_list:
        return True
    return False


def validate_url(_url: str, custom_scheme='http') -> bool:
    """ Validate the url. Currently, support the following schemes ['http', 'https', 'ftp', 'ftps']

    :param custom_scheme: will be appended in case of no scheme is attached with the _url.
    :param _url: need to validate
    :return: bool
    """

    # _url must be a string
    if not isinstance(_url, str):
        return False

    validate = URLValidator()
    validate.schemes.extend(SUPPORTED_SCHEMES)

    # To check whether it owns scheme or not
    _scheme = _url.strip().find('://')
    if _scheme == -1:
        if not check_scheme(custom_scheme, validate.schemes):
            return False
        # Adding default scheme if missing
        _url = custom_scheme + '://' + _url
    try:
        validate(_url.strip())
        return True
    except ValidationError as e:
        return False
