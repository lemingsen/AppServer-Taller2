"""Endpoints relacionados a formas de pago"""
from flask import jsonify
from appserver.controllers import api_bp
from appserver.services.shared_server_services import SharedServer


@api_bp.route('/payments', methods=['GET'])
def get_payment_methods():
    """Obtiene todos los métodos de pago disponibles"""
    shared_server = SharedServer()
    payment_methods = shared_server.get_payment_methods()
    return jsonify(payment_methods), 200



