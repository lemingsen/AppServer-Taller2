"""Endpoints relacionados a formas de pago"""
from flask import jsonify, request, abort
from appserver.controllers import api_bp
from appserver.services.payment_method_services import PaymentsService


@api_bp.route('/payments', methods=['POST'])
def add_payment_method():
    """Agrega un método de pago"""
    if not request.is_json:
        abort(400)
    payment_dict = request.get_json()
    payment_method = PaymentsService.add_payment_method(payment_dict)
    return jsonify(payment_method), 200


@api_bp.route('/payments/<string:payment_id>', methods=['PUT'])
def modify_payment_method(payment_id):
    """Modifica un metodo de pago"""
    if not request.is_json:
        abort(400)
    payment_dict = request.get_json()
    PaymentsService.modify_payment_method(payment_id, payment_dict)
    return jsonify(result='success'), 200


@api_bp.route('/payments', methods=['GET'])
def get_payment_methods():
    """Obtiene todos los métodos de pago disponibles"""
    payment_methods = PaymentsService.get_payment_methods()
    return jsonify(payment_methods), 200


@api_bp.route('/payments/<string:payment_id>', methods=['GET'])
def get_payment_method(payment_id):
    """Obtiene un método de pago"""
    payment_method = PaymentsService.get_payment_method(payment_id)
    return jsonify(payment_method), 200


@api_bp.route('/payments/<string:payment_id>', methods=['DELETE'])
def delete_payment_method(payment_id):
    """Borra un método de pago"""
    PaymentsService.delete_payment_method(payment_id)
    return jsonify(result='success'), 200
