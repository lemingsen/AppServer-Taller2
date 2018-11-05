"""User models"""
from appserver.data.base_mapper import BaseMapper
from appserver.models.category import CategorySchema


class CategoryMapper(BaseMapper):
    """User Model"""
    collection = 'categories'
    schema = CategorySchema()
