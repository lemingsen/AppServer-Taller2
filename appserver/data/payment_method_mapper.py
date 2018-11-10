"""payment method mapper"""
from appserver.models.payment_method import PaymentMethodSchema
from appserver.data.base_mapper import BaseMapper


class PaymentMethodMapper(BaseMapper):
    """payment method mapper"""
    collection = 'payment_methods'
    schema = PaymentMethodSchema()
