"""User models"""
from appserver.data.base_mapper import BaseMapper
from appserver.models.order import OrderSchema
from appserver.services.exceptions import ForbiddenError


class OrderMapper(BaseMapper):
    """User Model"""
    collection = 'orders'
    schema = OrderSchema()

    @classmethod
    def rate_purchase(cls, tracking_number, rating):
        """Rates a purchase after checking that it has not been rated before."""
        if OrderMapper.get_one({'tracking_number': tracking_number, 'rate': {'$exists': True}}):
            raise ForbiddenError('Order has already been rated')
        OrderMapper.find_one_and_update({'tracking_number': tracking_number},
                                        {'$set': {'rate': rating}})
