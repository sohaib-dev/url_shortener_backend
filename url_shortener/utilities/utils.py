"""
    It contains the utility methods.

"""

import traceback

from .CONSTANTS import CONFIGURATIONS


def api_version(method_name: str, version: str) -> str:
    """
    Used to decide the API at runtime.

    :param method_name:
    :param version:
    :return: method_name + version
    """
    _version_name = '_'.join(version.split('.'))
    method_version = method_name + _version_name
    return method_version


def get_request_extra_params(request, _api_version='N/A', _log_extra_params=CONFIGURATIONS.LOG_EXTRA_PARAMETERS.value):
    """
    Fill the LOG_EXTRA_PARAMETERS for logging.

    :param request:
    :param _api_version:
    :return:
    """

    _log_extra_params['api_path'] = 'api_path => ' + str(request.path_info)
    _log_extra_params['api_version'] = 'version=' + str(_api_version)

    return _log_extra_params


def log_exception_traceback(sys_module, _logger, log_params=CONFIGURATIONS.LOG_EXTRA_PARAMETERS):
    """
    It will return the exception traceback.

    :param sys_module:
    :param _logger:
    :param log_params:
    :return:
    """

    try:
        exc_type, exc_value, exc_traceback = sys_module.exc_info()
        _exception = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        return _exception

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys_module.exc_info()
        _exception = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        _logger.error(_exception, extra=log_params)
        return None

