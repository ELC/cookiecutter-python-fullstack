from flask import Blueprint, jsonify, Response

blueprint = Blueprint("errors", __name__)


@blueprint.app_errorhandler(Exception)
def error_handler(error: Exception) -> Response:
    message = {"ErrorType": type(error).__name__, "Message": str(error)}
    response = jsonify(message)
    response.status_code = 500
    return response
