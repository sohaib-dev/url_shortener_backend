"""
    It contains the Encoded-URL API. Currently, versioning only covers the encoding algorithm.
    Versioning is handled through Accept header. It will return 400 bad-request in case of any unhandled exception.

"""

import logging
import sys

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utilities.url_validators import validate_url
from utilities.base62 import base62encode
from utilities.CONSTANTS import CONFIGURATIONS, API_VERSIONS
from utilities import global_configurations
from utilities.utils import api_version, get_request_extra_params, log_exception_traceback

logger = logging.getLogger("ServicesLog")

class EncodeAPIVersioning:
    """
    Encode API versions
    """

    def encode_api_v1_0(self, _log_params=CONFIGURATIONS.LOG_EXTRA_PARAMETERS.value):
        """
        Encode the integer based on encoding algorithm

        :param _log_params:
        :return: _encoded_value, _counter_value
        """
        global_configurations.counter += 1
        _counter_value = global_configurations.counter
        _encoded_value = base62encode(_counter_value)

        logger.info('encode_api_v1_0 output, _counter_value : {}, _encoded_value : {} : '.format(
            _counter_value, _encoded_value), extra=_log_params)

        return _encoded_value, _counter_value


class EncodeURL(APIView, EncodeAPIVersioning):
    """
    Encode URL API's

    """

    def __init__(self):
        super().__init__()
        EncodeAPIVersioning.__init__(self)

    def post(self, request):
        """
        Encode URL Post API

        """

        try:
            _api_version = request.version if request.version else API_VERSIONS.ENCODE_API_DEFAULT_VERSION.value
            log_params = get_request_extra_params(request, _api_version, CONFIGURATIONS.LOG_EXTRA_PARAMETERS.value)
            _original_url = request.POST.get('original_url', '')

            logger.info('_original_url for encoding : ' + _original_url, extra=log_params)

            is_url_valid = validate_url(_original_url)
            if not is_url_valid:
                json_data = {
                    'status': 'False',
                    'ValidationError': 'URL is not valid'
                }
                logger.info('encode_api invalid URL response : ' + str(json_data), extra=log_params)

                return Response(json_data, content_type='application/json; version={}'.format(_api_version))

            _encode_method_name = 'encode_api_v'
            try:
                _encode_method_version = api_version(_encode_method_name, _api_version)
                encode_method = getattr(self, _encode_method_version)
            except AttributeError as e:
                _exception = log_exception_traceback(sys, logger, log_params)
                logger.info(_exception, extra=log_params)
                _api_version = API_VERSIONS.ENCODE_API_DEFAULT_VERSION
                _encode_method_version = api_version(_encode_method_name, _api_version)
                encode_method = getattr(self, _encode_method_version)

            short_url_encoded_value, _counter_value = encode_method(_log_params=log_params)
            global_configurations.url_mapping[_counter_value] = _original_url

            json_data = {
                'status': 'True',
                'short_url': short_url_encoded_value
            }
            logger.info('encode_api success response : ' + str(json_data), extra=log_params)

            return Response(json_data, content_type='application/json; version={}'.format(_api_version))

        except Exception as e:
            _exception = log_exception_traceback(sys, logger, log_params)
            logger.info(_exception, extra=log_params)

            json_data = {
                'status': 'False',
            }
            logger.info('encode_api unsuccessful response : ' + str(json_data), extra=log_params)

            return Response(json_data, status=status.HTTP_400_BAD_REQUEST,
                            content_type='application/json; version={}'.format(_api_version))
