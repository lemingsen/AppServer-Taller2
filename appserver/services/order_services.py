"""Order Services"""
import bson
from appserver.models.order import OrderSchema
from appserver.data.product_mapper import ProductMapper
from appserver.data.order_mapper import OrderMapper
from appserver.data.payment_method_mapper import PaymentMethodMapper
from appserver.services.exceptions import NotFoundError, NotEnoughUnitsError, ForbiddenError


class OrderServices:
    """Order Services"""
    schema = OrderSchema()

    @classmethod
    def new_order(cls, buyer_uid, order_data):
        """Creates a new purchase order of a product"""
        order = cls.schema.load(order_data)
        order.buyer = buyer_uid
        product = ProductMapper.get_by_id(order.product_id)
        if product is None:
            raise NotFoundError("Product not found.")
        if order.buyer == product.seller:
            raise ForbiddenError("User cannot buy his own products.")
        cls._validate_product_payment_method(
            order.payment_info.payment_method, product.payment_methods)
        cls._validate_payment_info(order.payment_info)
        order.seller = product.seller
        order.total = product.price * order.units
        order.product_name = product.name
        if order.units > product.units:
            raise NotEnoughUnitsError("Not enough units.")
        product = ProductMapper.find_one_and_update(
            {'_id': bson.ObjectId(product.id)},
            {'$inc': {'units': -order.units}}
        )
        if product.units < 0:
            ProductMapper.find_one_and_update(
                {'_id': bson.ObjectId(product.id)},
                {'$inc': {'units': order.units}}
            )
            raise NotEnoughUnitsError("Not enough units.")
        order_id = OrderMapper.insert(order)
        return order_id

    @classmethod
    def get_sales(cls, uid):
        """Returns all sales from a user"""
        orders = OrderMapper.get_many({'seller': uid})
        sales = []
        for order in orders:
            sales.append(cls.schema.dump(order))
        return sales

    @classmethod
    def get_purchases(cls, uid):
        """Returns all purchases from a user"""
        orders = OrderMapper.get_many({'buyer': uid})
        purchases = []
        for order in orders:
            purchases.append(cls.schema.dump(order))
        return purchases

    @classmethod
    def _validate_payment_info(cls, payment_info):
        payment_method = PaymentMethodMapper.get_one({'name': payment_info.payment_method})
        if payment_method is None:
            raise ForbiddenError("Invalid payment method.")
        if payment_method.type:
            cls._validate_card_info(payment_info)

    @classmethod
    def _validate_card_info(cls, payment_info):
        try:
            is_valid_card = payment_info.cardholder_name \
                         and payment_info.card_number \
                         and payment_info.expiration_date \
                         and payment_info.security_code
        except AttributeError:
            raise ForbiddenError("Missing payment info")
        return is_valid_card

    @classmethod
    def _validate_product_payment_method(cls, payment_method, product_payment_methods):
        found = False
        for product_payment_method in product_payment_methods:
            if payment_method == product_payment_method.name:
                found = True
                break
        if not found:
            raise ForbiddenError("Invalid payment method.")
