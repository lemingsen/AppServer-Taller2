"""Endpoints relacionados a ordenes de compra"""
from flask_jwt_extended import fresh_jwt_required, get_jwt_identity
from flask import jsonify, request, abort
from appserver.controllers import api_bp
from appserver.services.order_services import OrderServices


@api_bp.route('/orders', methods=['POST'])
@fresh_jwt_required
def new_order():
    """Servicio de compra: Este servicio permite realizar la compra
     de un producto que se encuentra publicado. Devuelve un código
     que identifica la compra de forma única y que permite conocer
     el estado de la misma (tracking)"""
    uid = get_jwt_identity()
    if not request.is_json:
        abort(400)
    purchase = request.get_json()
    purchase_id = OrderServices.new_order(uid, purchase)
    return jsonify(order_tracking_number=purchase_id), 200


@api_bp.route('/orders/tracking/<int:tracking_number>', methods=['GET'])
@fresh_jwt_required
def track_order(tracking_number):
    """Este servicio permitirá conocer el estado de
    una compra a través del código de tracking."""
    uid = get_jwt_identity()
    order = OrderServices.track_order(uid, tracking_number)
    return jsonify(order), 200


@api_bp.route('/orders/shipping/estimate/<int:tracking_number>', methods=['GET'])
@fresh_jwt_required
def estimate_order_shipping_cost(tracking_number):
    """Permite saber, con un margen de error, el costo de un
     envío antes de realizarlo. Este servicio será una
      fachada de uno proporcionado por el Shared Server."""
    cost = OrderServices.estimate_shipping_cost(tracking_number)
    return jsonify(estimated_cost=cost), 200


@api_bp.route('/orders/sales', methods=['GET'])
@fresh_jwt_required
def get_sales():
    """Devuelve las ventas realizadas por el usuario"""
    uid = get_jwt_identity()
    sales = OrderServices.get_sales(uid)
    return jsonify(count=len(sales), orders=sales), 200


@api_bp.route('/orders/purchases', methods=['GET'])
@fresh_jwt_required
def get_purchases():
    """Devuelve las compras realizadas por el usuario"""
    uid = get_jwt_identity()
    purchases = OrderServices.get_purchases(uid)
    return jsonify(count=len(purchases), orders=purchases), 200


@api_bp.route('/orders/ratings/<int:tracking_number>', methods=['POST'])
@fresh_jwt_required
def rate_purchase(tracking_number):
    """Permite calificar una compra"""
    uid = get_jwt_identity()
    if not request.is_json:
        abort(400)
    payload = request.get_json()
    OrderServices.rate_purchase(uid, tracking_number, payload)
    return jsonify(result='success'), 200
