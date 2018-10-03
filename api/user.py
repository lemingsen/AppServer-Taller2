"""Hello World"""
from firebase_admin import auth
import firebase_admin
from flask import abort
from flask import jsonify, request
from flask_jwt_extended import (
    fresh_jwt_required, create_access_token,
    get_jwt_identity
)
from api import api


def firebase_auth(data):
    """Autentica con firebase"""
    if 'idToken' not in data:
        abort(400)
    decoded_token = auth.verify_id_token(data['idToken'],
                                         firebase_admin.get_app(), check_revoked=True)
    return decoded_token


@api.route('/auth', methods=['POST'])
def login():
    """Servicio de autenticación: permite a los usuarios poder ingresar al sistema con
    un token de firebase, obteniendo un token para utilizar con los demás servicios."""
    decoded_token = firebase_auth(request.get_json())
    uid = decoded_token['uid']
    access_token = create_access_token(identity=uid, fresh=True, expires_delta=False)
    return jsonify(token=access_token)


@api.route('/register', methods=['POST'])
def register():
    """Servicio de registro: permite a los usuarios darse de alta en el sistema."""
    pass


@api.route('/profile', methods=['GET'])
@fresh_jwt_required
def get_profile():
    """Permite consultar el perfil de un usuario"""
    current_user = get_jwt_identity()
    return jsonify(uid=current_user)


@api.route('/profile', methods=['PUT'])
@fresh_jwt_required
def modify_profile():
    """Permite a un usuario actualizar su perfil"""
    pass
