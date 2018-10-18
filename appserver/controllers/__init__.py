"""controllers init"""
from flask import Blueprint
from firebase_admin import auth
import firebase_admin
from flask import abort


api = Blueprint('controllers', __name__)


def firebase_auth(data):
    """Autentica con firebase"""
    if 'idToken' not in data:
        abort(400)
    decoded_token = auth.verify_id_token(data['idToken'],
                                         firebase_admin.get_app(), check_revoked=True)
    return decoded_token


from appserver.controllers import root, user, products, errors
