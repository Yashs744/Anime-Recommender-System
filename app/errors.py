from flask import jsonify
from app import application
from app.constants import ErrorCodes
from http import HTTPStatus


@application.errorhandler(404)
def not_found_error(error):
    return error_response(error_code=ErrorCodes.API_NOT_FOUND, status_code=HTTPStatus.NOT_FOUND.value)


@application.errorhandler(405)
def method_not_allowed_error(error):
    return error_response(error_code=ErrorCodes.METHOD_NOT_ALLOWED, status_code=HTTPStatus.METHOD_NOT_ALLOWED.value)


def error_response(error_code, status_code):
    """
    Generic method to return error response

    :param error_code: ``ErrorCodes``
        Enum
    :param status_code: ``int``
        HTTP status code of response
    :return:
    """

    return jsonify(
        status='failure',
        error_code=error_code.value,
        description=error_code.description
    ), status_code
