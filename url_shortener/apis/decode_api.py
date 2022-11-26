"""
    It contains the Decode-URL API. Decode the URL encoded by the encode_url API.

"""

import logging
import sys

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utilities.base62 import base62decode
from utilities import global_configurations
from utilities.CONSTANTS import CONFIGURATIONS, API_VERSIONS
from utilities.utils import api_version, log_exception_traceback, get_request_extra_params

logger = logging.getLogger("ServicesLog")


class DecodeAPIVersioning:
    """
    Encode API versions

    """

    def decode_api_v1_0(self, _short_url: str, _log_params=CONFIGURATIONS.LOG_EXTRA_PARAMETERS) -> int:
        """
        Decode the short_url based on decoding algorithm

        :param _short_url:
        :param _log_params:
        :return: _decoded_value
        """

        try:
            _decoded_value = base62decode(_short_url)
            logger.info('decode_api_v1_0 output, _decoded_value : {} '.format(_decoded_value), extra=_log_params)
        except Exception:
            _exception = log_exception_traceback(sys, logger, _log_params)
            logger.info(_exception, extra=_log_params)
            _decoded_value = ''

        return _decoded_value


class DecodeURL(APIView, DecodeAPIVersioning):
    """
    Decode URL API

    """

    def __init__(self):
        super().__init__()
        DecodeAPIVersioning.__init__(self)

    def post(self, request, format=None):
        """
        Decode-URL post API.

        """
        try:
            _api_version = request.version if request.version else API_VERSIONS.DECODE_API_DEFAULT_VERSION.value
            log_params = get_request_extra_params(request, _api_version, CONFIGURATIONS.LOG_EXTRA_PARAMETERS.value)
            _short_url = request.POST.get('short_url', '')

            logger.info('_short_url for decoding : ' + _short_url, extra=log_params)

            _decode_method_name = 'decode_api_v'
            try:
                _encode_method_version = api_version(_decode_method_name, _api_version)
                _decode_method = getattr(self, _encode_method_version)
            except AttributeError:
                _exception = log_exception_traceback(sys, logger, log_params)
                logger.info(_exception, extra=log_params)
                _api_version = API_VERSIONS.DECODE_API_DEFAULT_VERSION.value
                _encode_method_version = api_version(_decode_method_name, _api_version)
                _decode_method = getattr(self, _encode_method_version)

            _decoded_value = _decode_method(_short_url, log_params)
            if _decoded_value:
                try:
                    _original_url = global_configurations.url_mapping[_decoded_value]
                except KeyError:
                    _exception = log_exception_traceback(sys, logger, log_params)
                    logger.info(_exception, extra=log_params)

                    json_data = {
                        'status': 'False',
                        'ValidationError': 'This short-URL not found in the system'
                    }
                    logger.info('decode_api short-url not found response ' + str(json_data), extra=log_params)

                    return Response(json_data, content_type='application/json; version={}'.format(_api_version))
            else:
                json_data = {
                    'status': 'False',
                    'ValidationError': 'Short-URL cannot be Decoded'
                }
                logger.info('decode_api short-url not decoded response ' + str(json_data), extra=log_params)

                return Response(json_data, content_type='application/json; version={}'.format(_api_version))

            json_data = {
                'status': 'True',
                'original_url': _original_url
            }
            logger.info('decode_api success response ' + str(json_data), extra=log_params)

            return Response(json_data, content_type='application/json; version={}'.format(_api_version))

        except Exception:
            _exception = log_exception_traceback(sys, logger, log_params)
            logger.info(_exception, extra=log_params)

            json_data = {
                'status': 'False',
            }
            logger.info('decode_api unsuccessful response ' + str(json_data), extra=log_params)

            return Response(json_data, status=status.HTTP_400_BAD_REQUEST,
                            content_type='application/json; version={}'.format(_api_version))
