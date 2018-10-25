"""product model"""
from appserver.model.product import ProductSchema
from appserver.data.base_mapper import BaseMapper


class ProductMapper(BaseMapper):
    """product model"""
    collection = 'products'
    schema = ProductSchema()
