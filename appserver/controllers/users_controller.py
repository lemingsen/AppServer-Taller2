"""Endpoints relacionados al usuario"""
from flask import jsonify, request, abort
from flask_jwt_extended import fresh_jwt_required, get_jwt_identity
import requests
from appserver.controllers import api_bp
from appserver.service.users_service import UserService


@api_bp.route('/user/auth', methods=['POST'])
def login():
    """Servicio de autenticación: permite a los usuarios poder ingresar al sistema con
    un token de firebase, obteniendo un token para utilizar con los demás servicios."""
    if not request.is_json:
        abort(400)
    firebase_token = request.get_json()
    access_token = UserService.login(firebase_token)
    return jsonify(token=access_token), 200


@api_bp.route('/user/register', methods=['POST'])
def register():
    """Servicio de registro: permite a los usuarios darse de alta en el sistema."""
    if not request.is_json:
        abort(400)
    data = request.get_json()
    uid = UserService.register(data)
    return jsonify(result='success', uid=uid), 200


@api_bp.route('/user/profile', methods=['GET'])
@fresh_jwt_required
def get_profile():
    """Permite consultar el perfil de un usuario"""
    uid = get_jwt_identity()
    user = UserService.get_profile(uid)
    return jsonify(user), 200


@api_bp.route('/user/profile', methods=['PUT'])
@fresh_jwt_required
def modify_profile():
    """Permite a un usuario actualizar su perfil"""
    if not request.is_json:
        abort(400)
    data = request.get_json()
    uid = get_jwt_identity()
    UserService.modify_profile(uid, data)
    return jsonify(result='success'), 200


@api_bp.route('/user/purchases', methods=['GET'])
@fresh_jwt_required
def my_purchases():
    """Devuelve un listado de las compras del usuario"""
    return jsonify(message="ok"), 200


@api_bp.route('/user/publications', methods=['GET'])
@fresh_jwt_required
def my_publications():
    """Devuelve un listado de las publicaciones del usuario"""
    pass


@api_bp.route('/user/sales', methods=['GET'])
@fresh_jwt_required
def my_sales():
    """Devuelve un listado de las ventas del usuario"""
    pass


@api_bp.route('/user/purchases/<string:track_id>', methods=['GET'])
def track(track_id):
    """Servicio de tracking: permite conocer el estado de una
     compra a través del código de tracking"""
    req = requests.get('https://shared-server-tallerii.herokuapp.com/envios/' + str(track_id))
    return req.json()
