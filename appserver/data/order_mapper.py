"""User models"""
from appserver.data.base_mapper import BaseMapper
from appserver.models.order import OrderSchema


class OrderMapper(BaseMapper):
    """User Model"""
    collection = 'orders'
    schema = OrderSchema()
