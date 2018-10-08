"""api init"""
from flask import Blueprint
from flask import jsonify
from firebase_admin.auth import AuthError
from firebase_admin import auth
import firebase_admin
from flask import abort


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


def firebase_auth(data):
    """Autentica con firebase"""
    if 'idToken' not in data:
        abort(400)
    decoded_token = auth.verify_id_token(data['idToken'],
                                         firebase_admin.get_app(), check_revoked=True)
    return decoded_token


from api import root, user, products
