"""Endpoints relacionados al usuario"""
from flask import jsonify, request
from flask_jwt_extended import (
    fresh_jwt_required, create_access_token,
    get_jwt_identity
)
import requests
from api import firebase_auth
from api import api
from models.user import User
import datetime


@api.route('/user/auth', methods=['POST'])
def login():
    """Servicio de autenticación: permite a los usuarios poder ingresar al sistema con
    un token de firebase, obteniendo un token para utilizar con los demás servicios."""
    decoded_token = firebase_auth(request.get_json())
    uid = decoded_token['uid']
    access_token = create_access_token(identity=uid, fresh=True, expires_delta=False)
    return jsonify(token=access_token, uid=uid)


@api.route('/user/register', methods=['POST'])
def register():
    """Servicio de registro: permite a los usuarios darse de alta en el sistema."""
    data = request.get_json()
    User.insert(data)
    return jsonify(result='ok')


@api.route('/user/profile', methods=['GET'])
@fresh_jwt_required
def get_profile():
    """Permite consultar el perfil de un usuario"""
    current_user = get_jwt_identity()
    return jsonify(uid=current_user, name="Nombre", surname="Apellido", email="nombre@gmail.com",
                   facebook="123342342342", google="nombre@gmail.com",
                   photo="https://www.iemoji.com/view/emoji/1336/skin-tones/man-medium-skin-tone",
                   member_since=datetime.datetime.now(), last_login=datetime.datetime.now())


@api.route('/user/profile', methods=['PUT'])
@fresh_jwt_required
def modify_profile():
    """Permite a un usuario actualizar su perfil"""
    pass


@api.route('/user/purchases', methods=['GET'])
@fresh_jwt_required
def my_purchases():
    """Devuelve un listado de las compras del usuario"""
    pass


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
