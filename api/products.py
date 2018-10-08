"""Endpoints relacionados a productos"""
from flask_jwt_extended import fresh_jwt_required
from api import api


@api.route('/products', methods=['GET'])
@fresh_jwt_required
def get_products():
    """Servicio de búsqueda de productos: Devuelve un listado
     de productos utilizando varios de sus atributos como filtros"""
    pass


@api.route('/products/<string:product_id>', methods=['GET'])
@fresh_jwt_required
def get_product(product_id):
    """Devuelve un producto por su id"""
    pass


@api.route('/products/<string:product_id>/buy', methods=['POST'])
@fresh_jwt_required
def buy_product(product_id):
    """Servicio de compra: Este servicio permite realizar la compra
     de un producto que se encuentra publicado. Devuelve un código
     que identifica la compra de forma única y que permite conocer
     el estado de la misma (tracking)"""
    pass


@api.route('/products', methods=['POST'])
@fresh_jwt_required
def add_product():
    """Servicio de publicación de articulo para la venta"""
    pass


@api.route('/products/<string:product_id>/questions', methods=['POST'])
@fresh_jwt_required
def add_product_question(product_id):
    """Servicio de alta de pregunta: permite realizar una pregunta
     acerca de un artículo que se encuentra publicado para la venta"""
    pass


@api.route('/products/<string:product_id>/<string:question_id>/answers', methods=['POST'])
@fresh_jwt_required
def add_product_answer(product_id, question_id):
    """Servicio de alta de respuesta a pregunta:
    permite responder una pregunta que fue realizada."""
    pass
