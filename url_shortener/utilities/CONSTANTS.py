"""
    All application constants resides here. We can store these configurations in the database as well.
"""

from enum import Enum


class BASE62(Enum):
    """
    Base62 enums
    """
    # BASE62_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    BASE62_CHARSET = "a0ABCD1EFGHIKLMNOPQRSUVW4XYZabde5fghjklm6nopqrs7tuvw8xyz9"
    BASE62_CHARSET_INVERTED = BASE62_CHARSET[::-1]
    BASE62_LENGTH = int(len(BASE62_CHARSET))

    RANDOM_GENERATOR_CHARSET = {'J', '2', '7', 'T', 'c'}
    RANDOM_GENERATOR_CHARSET_LENGTH = len(RANDOM_GENERATOR_CHARSET)
    SPLITTING_CHARSET = '3i'
    SPLITTING_CHARSET_LENGTH = len(SPLITTING_CHARSET)


class API_VERSIONS(Enum):
    ENCODE_API_DEFAULT_VERSION = '1.0'
    DECODE_API_DEFAULT_VERSION = '1.0'


class CONFIGURATIONS(Enum):
    LOG_EXTRA_PARAMETERS = {
        'api_path': 'N/A',
        'api_version': 'N/A',
    }
