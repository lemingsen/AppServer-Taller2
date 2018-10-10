"""Endpoints relacionados al usuario"""
from flask import jsonify, request, abort
from flask_jwt_extended import (
    fresh_jwt_required, create_access_token,
    get_jwt_identity
)
import requests
from datetime import datetime
from api import firebase_auth, api
from models.user import User, UserSchema


@api.route('/user/auth', methods=['POST'])
def login():
    """Servicio de autenticación: permite a los usuarios poder ingresar al sistema con
    un token de firebase, obteniendo un token para utilizar con los demás servicios."""
    decoded_token = firebase_auth(request.get_json())
    uid = decoded_token['uid']
    access_token = create_access_token(identity=uid, fresh=True, expires_delta=False)
    return jsonify(token=access_token, uid=uid), 200


@api.route('/user/register', methods=['POST'])
def register():
    """Servicio de registro: permite a los usuarios darse de alta en el sistema."""
    if not request.is_json:
        abort(400)
    data = request.get_json()
    schema = UserSchema()
    if User.get_one({"uid": data["uid"]}) is not None:
        abort(409)
    data["member_since"] = str(datetime.now())
    data["last_login"] = str(datetime.now())
    User.insert(schema.load(data))
    return jsonify(result='success'), 200


@api.route('/user/profile', methods=['GET'])
@fresh_jwt_required
def get_profile():
    """Permite consultar el perfil de un usuario"""
    current_user = get_jwt_identity()
    user = User.get_one_or_404({"uid": current_user})
    return jsonify(user), 200


@api.route('/user/profile', methods=['PUT'])
@fresh_jwt_required
def modify_profile():
    """Permite a un usuario actualizar su perfil"""
    if not request.is_json:
        abort(400)
    data = request.get_json()
    current_user = get_jwt_identity()
    schema = UserSchema()
    ret = User.modify({"uid": current_user}, schema.load(data))
    return jsonify(ret), 200


@api.route('/user/purchases', methods=['GET'])
@fresh_jwt_required
def my_purchases():
    """Devuelve un listado de las compras del usuario"""
    return jsonify(message="ok"), 200


@api.route('/user/publications', methods=['GET'])
@fresh_jwt_required
def my_publications():
    """Devuelve un listado de las publicaciones del usuario"""
    pass


@api.route('/user/sales', methods=['GET'])
@fresh_jwt_required
def my_sales():
    """Devuelve un listado de las ventas del usuario"""
    pass


@api.route('/user/purchases/<string:track_id>', methods=['GET'])
def track(track_id):
    """Servicio de tracking: permite conocer el estado de una
     compra a través del código de tracking"""
    req = requests.get('https://shared-server-tallerii.herokuapp.com/envios/' + str(track_id))
    return req.json()
