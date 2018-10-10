"""Error handlers"""
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized, NotFound
from marshmallow import ValidationError
from flask import jsonify
from firebase_admin.auth import AuthError
from api import api


@api.app_errorhandler(NotFound)
def not_found_error_handle(error):
    """Error handler para error 404 (Not Found)"""
    return jsonify(error=NotFound.description), 404


@api.app_errorhandler(ValueError)
@api.app_errorhandler(AuthError)
@api.app_errorhandler(Unauthorized)
def value_error_error_handler(error):
    """Error handler para error 401 (Unauthorized)"""
    return jsonify(error=Unauthorized.description), 401


@api.app_errorhandler(BadRequest)
def bad_request_error_handler(error):
    """Error handler para error 400 (Bad Request)"""
    return jsonify(error=BadRequest.description), 400


@api.app_errorhandler(Conflict)
def conflict_error_handler(error):
    """Error handler para error 409 (Conflict)"""
    return jsonify(error=Conflict.description), 409


@api.app_errorhandler(ValidationError)
def validation_error_handler(error):
    """Error handler para errores de validación"""
    return jsonify(error=BadRequest.description, validation_error=error.messages), 400
