"""Order Services"""
import bson
from marshmallow.exceptions import ValidationError
from appserver.models.order import OrderSchema
from appserver.data.product_mapper import ProductMapper
from appserver.data.order_mapper import OrderMapper
from appserver.services.exceptions import NotFoundError, NotEnoughUnitsError, ForbiddenError
from appserver.services.shared_server_services import SharedServer
from appserver.data.user_mapper import UserMapper


class OrderServices:
    """Order Services"""
    schema = OrderSchema()

    @classmethod
    def new_order(cls, buyer_uid, order_data):
        """Creates a new purchase order of a product"""
        order = cls.schema.load(order_data)
        product = cls._get_product(order.product_id)
        buyer = cls._get_buyer(buyer_uid)
        order.buyer = buyer_uid
        order.seller = product.seller
        order.total = product.price * order.units
        order.buyer_location = buyer.location
        order.product_location = product.location
        order.product_name = product.name
        cls._validate_order(order, product)
        cls._update_product(order, product)
        shared_server = SharedServer()
        order.tracking_number = shared_server.new_tracking()
        shared_server.create_payment(order)
        order.status = 'COMPRA REALIZADA'
        OrderMapper.insert(order)
        return order.tracking_number

    @classmethod
    def track_order(cls, buyer_uid, tracking_number):
        """Track order service: gets order status from shared server"""
        order = cls._get_order(tracking_number)
        if order.buyer != buyer_uid:
            raise ForbiddenError("Order does not belong to user")
        if order.status != 'ENVIO REALIZADO':
            cls._update_tracking_status(order)
        return cls.schema.dump(order)

    @classmethod
    def estimate_shipping_cost(cls, tracking_number):
        """Estimates order shipping cost"""
        order = cls._get_order(tracking_number)
        buyer = cls._get_buyer(order.buyer)
        shared_server = SharedServer()
        shipping_cost = shared_server.get_delivery_estimate(order, buyer)
        return shipping_cost

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
    def review_purchase(cls, uid, tracking_number, review_dict):
        """Reviews a purchase"""
        order = cls._get_order(tracking_number)
        if order.buyer != uid:
            raise ForbiddenError("You can review your own purchases.")
        if order.status != "ENVIO REALIZADO":
            raise ForbiddenError("Cannot review purchase until order is delivered.")
        if review_dict.get('review') is None:
            raise ValidationError("No review sent")
        OrderMapper.find_one_and_update({'tracking_number': tracking_number},
                                        {'$set': {'review': review_dict.get('review')}})

    @classmethod
    def _update_tracking_status(cls, order):
        missing_payment = ['COMPRA_REALIZADA', 'PAGO PENDIENTE DE PROCESO', 'PAGO RECHAZADO']
        missing_delivery = ['PAGO ACEPTADO', 'ENVIO EN PROGRESO',
                            'PENDIENTE DE ENVIO', 'ENVIO CANCELADO']
        shared_server = SharedServer()
        if order.status in missing_payment:
            shared_server.update_payment_status(order)
        if order.status in missing_delivery:
            shared_server.update_tracking_status(order)

    @classmethod
    def _get_order(cls, tracking_number):
        order = OrderMapper.get_one({'tracking_number': tracking_number})
        if order is None:
            raise NotFoundError("Order not found.")
        return order

    @classmethod
    def _validate_order(cls, order, product):
        if order.buyer == product.seller:
            raise ForbiddenError("User cannot buy his own products.")
        cls._validate_product_has_payment_method(
            order.payment_info, product.payment_methods)

    @classmethod
    def _validate_product_has_payment_method(cls, payment_info, product_payment_methods):
        found = False
        for product_payment_method in product_payment_methods:
            if payment_info.payment_method == product_payment_method.name:
                found = True
                if product_payment_method.type == 1:
                    cls._validate_credit_card_info(payment_info)
                break
        if not found:
            raise ForbiddenError("Invalid payment method.")

    @classmethod
    def _validate_credit_card_info(cls, payment_info):
        try:
            is_valid_card = payment_info.cardholder_name \
                         and payment_info.card_number \
                         and payment_info.expiration_date \
                         and payment_info.security_code
        except AttributeError:
            raise ForbiddenError("Missing credit card payment information")
        return is_valid_card

    @classmethod
    def _update_product(cls, order, product):
        if order.units > product.units:
            raise NotEnoughUnitsError("Not enough units.")
        product = cls._update_product_units(order, product)
        if product.units < 0:
            cls._rollback_product_units_update(order, product)
            raise NotEnoughUnitsError("Not enough units.")

    @classmethod
    def _rollback_product_units_update(cls, order, product):
        ProductMapper.find_one_and_update(
            {'_id': bson.ObjectId(product.id)},
            {'$inc': {'units': order.units}}
        )

    @classmethod
    def _update_product_units(cls, order, product):
        return ProductMapper.find_one_and_update(
            {'_id': bson.ObjectId(product.id)},
            {'$inc': {'units': -order.units}}
        )

    @classmethod
    def _get_product(cls, product_id):
        product = ProductMapper.get_by_id(product_id)
        if product is None:
            raise NotFoundError("Product not found.")
        return product

    @classmethod
    def _get_buyer(cls, buyer_uid):
        buyer = UserMapper.get_one({'uid': buyer_uid})
        if buyer is None:
            raise NotFoundError("User not found.")
        return buyer
