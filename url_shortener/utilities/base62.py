"""
    base62 data encodings.
"""

import logging
import random

from .CONSTANTS import BASE62, CONFIGURATIONS

logger = logging.getLogger("ServicesLog")


def base62encode(num: int, min_len=7, char_set=BASE62.BASE62_CHARSET.value, _log_params=CONFIGURATIONS.LOG_EXTRA_PARAMETERS.value):
    """
    Encoding an integer to base62 string.

    :param num: number to be encoded
    :param min_len: default 7
    :param char_set: Default base62
    :param _log_params:
    :return: encoded str
    """

    _chars_str = ''
    _rdivmod = divmod
    base = int(len(char_set))
    logger.info('base62encode : encode the number : {}.'.format(num), extra=_log_params)

    while num > 0:
        num, _remainder = _rdivmod(num, base)
        _chars_str = _chars_str + char_set[_remainder]

    _chars_str = _chars_str[::-1]
    logger.info('base62encode : encoded character string : {}.'.format(_chars_str), extra=_log_params)

    # Append extra characters in case of encoded string has fewer characters.
    required_url_len = min_len - len(_chars_str)

    if required_url_len:
        list_of_random_chars = random.sample(BASE62.RANDOM_GENERATOR_CHARSET.value, BASE62.RANDOM_GENERATOR_CHARSET_LENGTH.value)
        generated_random_str = ''.join(list_of_random_chars)

        _chars_str = generated_random_str[:required_url_len - 1] + \
                     BASE62.SPLITTING_CHARSET.value[random.randint(0, BASE62.SPLITTING_CHARSET_LENGTH.value - 1)] + _chars_str

    _encoded_str = _chars_str
    logger.info('base62encode : encoded value : {} for number : {}'.format(_chars_str, num), extra=_log_params)

    return _encoded_str


def actual_encoded_str(encoded_str: str, _log_params=CONFIGURATIONS.LOG_EXTRA_PARAMETERS.value):
    """

    :param encoded_str: Dummy encoded string
    :param _log_params:
    :return: actual encoded string after removing random characters.
    """

    common_char_set = set(BASE62.SPLITTING_CHARSET.value).intersection(encoded_str)
    common_char = common_char_set.pop()
    actual_encoded_value = encoded_str.split(common_char)[1]

    logger.info('actual_encoded_str : got the actual_encoded_value : {}, from the input encoded_str : {}.'.format(
        actual_encoded_value, encoded_str), extra=_log_params)

    return actual_encoded_value


def base62decode(encoded_str: str, char_set=BASE62.BASE62_CHARSET.value, _log_params=CONFIGURATIONS.LOG_EXTRA_PARAMETERS.value):
    """ Decode the string encoded by base62encode.

    :param encoded_str:
    :param char_set:
    :param _log_params:
    :return:
    """

    if not isinstance(encoded_str, str):
        return False

    # Get the actual encoded string
    _encoded_str = actual_encoded_str(encoded_str)
    logger.info('base62decode : encoded value : {} to decode'.format(_encoded_str), extra=_log_params)

    _decoded_integer, _reduce_num = 0, 0
    _encoded_str_len = len(_encoded_str)

    for char in _encoded_str:
        _reduce_num += 1
        _decoded_integer += char_set.index(char) * (BASE62.BASE62_LENGTH.value ** (_encoded_str_len - _reduce_num))

    logger.info('base62decode : decoded number : {}, for encoded value : {}.'.format(_decoded_integer, _encoded_str),
                extra=_log_params)

    return _decoded_integer
