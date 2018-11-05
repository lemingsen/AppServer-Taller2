"""Endpoints relacionados a productos"""
from flask_jwt_extended import fresh_jwt_required, get_jwt_identity
from flask import jsonify, request, abort
from appserver.controllers import api_bp
from appserver.services.product_services import ProductsService
# pylint: disable=W0613


@api_bp.route('/products', methods=['GET'])
@fresh_jwt_required
def get_products():
    """Servicio de búsqueda de productos: Devuelve un listado
     de productos utilizando varios de sus atributos como filtros"""
    products = ProductsService.get_products(request.args.to_dict(flat=False))
    return jsonify(count=len(products), result=products), 200


@api_bp.route('/products/<string:product_id>', methods=['GET'])
@fresh_jwt_required
def get_product(product_id):
    """Devuelve un producto por su id"""
    product = ProductsService.get_product_by_id(product_id)
    return jsonify(product), 200


@api_bp.route('/products', methods=['POST'])
@fresh_jwt_required
def add_product():
    """Servicio de publicación de articulo para la venta"""
    uid = get_jwt_identity()
    if not request.is_json:
        abort(400)
    product = request.get_json()
    product_id = ProductsService.add_product(product, uid)
    return jsonify(result='success', _id=product_id), 200


@api_bp.route('/products/<string:product_id>', methods=['DELETE'])
@fresh_jwt_required
def delete_product(product_id):
    """Servicio de eliminación de un artículo"""
    uid = get_jwt_identity()
    ProductsService.delete_product(uid, product_id)
    return jsonify(result='success'), 200


@api_bp.route('/products/<string:product_id>/questions', methods=['POST'])
@fresh_jwt_required
def add_product_question(product_id):
    """Servicio de alta de pregunta: permite realizar una pregunta
     acerca de un artículo que se encuentra publicado para la venta"""
    uid = get_jwt_identity()
    if not request.is_json:
        abort(400)
    question = request.get_json()
    product = ProductsService.add_question(question, product_id, uid)
    return jsonify(product), 200


@api_bp.route('/products/<string:product_id>/questions/<string:question_id>/answers',
              methods=['POST'])
@fresh_jwt_required
def add_product_answer(product_id, question_id):
    """Servicio de alta de respuesta a pregunta:
    permite responder una pregunta que fue realizada."""
    uid = get_jwt_identity()
    if not request.is_json:
        abort(400)
    answer = request.get_json()
    product = ProductsService.add_answer(answer, product_id, question_id, uid)
    return jsonify(product), 200


@api_bp.route('/products/categories', methods=['GET'])
@fresh_jwt_required
def get_categories():
    """Devuelve las categorías de productos existentes"""
    categories = ProductsService.get_categories()
    return jsonify(categories), 200


@api_bp.route('/products/categories', methods=['POST'])
def add_category():
    """Agrega una categoría de productos"""
    if not request.is_json:
        abort(400)
    category = request.get_json()
    ProductsService.add_category(category)
    return jsonify(result='success'), 200


@api_bp.route('/products/categories/<string:category_id>', methods=['PUT'])
def modify_category(category_id):
    """Modifica una categoría de producto"""
    if not request.is_json:
        abort(400)
    category = request.get_json()
    ProductsService.modify_category(category_id, category)
    return jsonify(result='success'), 200


@api_bp.route('/products/categories/<string:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Borra la categoría de productos especificada por su id"""
    ProductsService.delete_category(category_id)
    return jsonify(result='success'), 200
