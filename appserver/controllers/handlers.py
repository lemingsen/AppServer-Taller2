"""Error handlers"""
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized,\
    NotFound, Forbidden, UnprocessableEntity, BadGateway
from marshmallow import ValidationError
from flask import jsonify
from firebase_admin.auth import AuthError
from appserver.controllers import api_bp
from appserver.services.exceptions import DataExistsError, NotFoundError,\
    ForbiddenError, NotEnoughUnitsError
# pylint: disable=W0613


@api_bp.app_errorhandler(NotFoundError)
def not_found_error_handler(error):
    """Error handler para recursos no encontrados (Not Found)"""
    return jsonify(error=NotFound.code, message=error.message,
                   description=NotFound.description), 404


@api_bp.app_errorhandler(ValueError)
@api_bp.app_errorhandler(AuthError)
@api_bp.app_errorhandler(Unauthorized)
def value_error_error_handler(error):
    """Error handler para error 401 (Unauthorized)"""
    return jsonify(error=Unauthorized.description), 401


@api_bp.app_errorhandler(BadRequest)
def bad_request_error_handler(error):
    """Error handler para error 400 (Bad Request)"""
    return jsonify(error=BadRequest.description), 400


@api_bp.app_errorhandler(DataExistsError)
def conflict_error_handler(error):
    """Error handler para error 409 (Conflict)"""
    return jsonify(error=Conflict.code, message=error.message,
                   description=Conflict.description), 409


@api_bp.app_errorhandler(ValidationError)
def validation_error_handler(error):
    """Error handler para errores de validación"""
    return jsonify(error=BadRequest.description, validation_error=error.messages), 400


@api_bp.app_errorhandler(ForbiddenError)
def forbidden_error_handler(error):
    """Error handler para operaciones no permitidas"""
    return jsonify(error=Forbidden.description, message=error.message), 403


@api_bp.app_errorhandler(NotEnoughUnitsError)
def not_enough_units_error_handler(error):
    """Error handler para compras sin recursos"""
    return jsonify(error=UnprocessableEntity.description, message=error.message), 422


@api_bp.app_errorhandler(BadGateway)
def bad_gateway_error_handler(error):
    """Error handler para errores de conexión con el shared server"""
    return jsonify(error=BadGateway.description), 502
