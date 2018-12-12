"""User models"""
from appserver.data.base_mapper import BaseMapper
from appserver.models.order import OrderSchema
from appserver.services.exceptions import ForbiddenError
from appserver.services.exceptions import NotFoundError


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

    @classmethod
    def update_status(cls, order):
        """Updates the status and last_status_update of an order"""
        order = OrderMapper.find_one_and_update(
            {'tracking_number': order.tracking_number},
            {'$set': {'status': order.status,
                      'last_status_update': order.last_status_update}}
        )
        if order is None:
            raise NotFoundError("Cannot update order status because order was not found.")
