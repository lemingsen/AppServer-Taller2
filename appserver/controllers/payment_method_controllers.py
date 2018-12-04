"""Endpoints relacionados a formas de pago"""
from flask import jsonify
from appserver.controllers import api_bp
from appserver.services.shared_server_services import SharedServer
from appserver.models.payment_method import PaymentMethodSchema


@api_bp.route('/payments', methods=['GET'])
def get_payment_methods():
    """Obtiene todos los métodos de pago disponibles"""
    payment_methods = SharedServer().get_payment_methods()
    payment_methods_dict = []
    for payment_method in payment_methods:
        payment_methods_dict.append(PaymentMethodSchema().dump(payment_method))
    return jsonify(payment_methods_dict), 200
