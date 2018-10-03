"""api init"""
from flask import Blueprint
from flask import jsonify
from firebase_admin.auth import AuthError

api = Blueprint('api', __name__)


@api.app_errorhandler(404)
def error_handler_not_found(error):
    """Error handler para error 404 (Not Found)"""
    return jsonify(error='404')


@api.app_errorhandler(ValueError)
@api.app_errorhandler(AuthError)
def value_error_handler(error):
    """Error handler para la autenticación con firebase"""
    return jsonify(error='ValueError')




from api import root, user, purchases, products
