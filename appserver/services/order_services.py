"""Order Services"""
import bson
from appserver.models.order import OrderSchema
from appserver.data.product_mapper import ProductMapper
from appserver.data.order_mapper import OrderMapper
from appserver.services.exceptions import NotFoundError, NotEnoughUnitsError


class OrderServices:
    """Order Services"""
    schema = OrderSchema()

    @classmethod
    def new_order(cls, buyer, order_data):
        """Creates a new purchase order of a product"""
        order = cls.schema.load(order_data)
        order.buyer = buyer
        product = ProductMapper.get_by_id(order.product_id)
        if product is None:
            raise NotFoundError("Product not found.")
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
