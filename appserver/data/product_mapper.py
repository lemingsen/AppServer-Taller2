"""product models"""
from appserver.models.product import ProductSchema
from appserver.data.base_mapper import BaseMapper


class ProductMapper(BaseMapper):
    """product models"""
    collection = 'products'
    schema = ProductSchema()
