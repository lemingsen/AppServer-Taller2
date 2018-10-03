"""Hello World"""
from flask_restplus import Namespace, Resource
from firebase_admin import auth
from firebase_admin.auth import AuthError
import firebase_admin
from flask import abort
from flask import jsonify, request
from flask_jwt_extended import (
    fresh_jwt_required, create_access_token,
    get_jwt_identity
)

ns = Namespace('user', description='/user')


def firebase_auth(data):
    """Autentica con firebase"""
    if 'idToken' not in data:
        abort(400)
    try:
        decoded_token = auth.verify_id_token(data['idToken'],
                                             firebase_admin.get_app(), check_revoked=True)
    except (ValueError, AuthError):
        abort(401)
    return decoded_token


@ns.route('/auth')
class Login(Resource):
    """Servicio de autenticación"""

    def post(self):
        """Permite a los usuarios poder ingresar al sistema, obteniendo
             un token que deberá ser utilizado por los demás servicios."""
        decoded_token = firebase_auth(request.get_json())
        uid = decoded_token['uid']
        access_token = create_access_token(identity=uid, fresh=True, expires_delta=False)
        return jsonify(token=access_token)


@ns.route('/register')
class Register(Resource):
    """Servicio de registro"""
    def post(self):
        """Permite a los usuarios darse de alta en el sistema."""
        pass


@ns.route('/profile')
class Profile(Resource):
    """Servicio de perfil de usuario"""

    @fresh_jwt_required
    def get(self):
        """Permite consultar el perfil de un usuario"""
        current_user = get_jwt_identity()
        return jsonify(uid=current_user)

    def put(self):
        """Permite a un usuario actualizar su perfil"""
        pass
