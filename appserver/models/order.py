"""Order model"""
from marshmallow import Schema, fields, post_load, validates, ValidationError, validate
from appserver.utils.mongo import ObjectId
# pylint: disable=R0903,R0201


class Order:
    """Order"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class OrderSchema(Schema):
    """marshmallow order schema"""
    _id = ObjectId()
    product_id = ObjectId(required=True)
    product_name = fields.Str(validate=validate.Length(
        min=1, error="Product name cannot be empty"))
    units = fields.Int(required=True)
    unit_price = fields.Float()
    payment_method = fields.Str(required=True, validate=validate.Length(
        min=1, error="Payment method cannot be empty."))
    datetime = fields.Str()
    buyer = fields.Str()
    seller = fields.Str()
    total = fields.Float()

    @validates('units')
    def validate_units(self, value):
        """Validates that order units are greater than zero"""
        if value <= 0:
            raise ValidationError("Order units must be greater than 0.")

    @validates('unit_price')
    def validate_unit_price(self, value):
        """Validates that order unit price is greater than zero"""
        if value <= 0:
            raise ValidationError("Order unit_price must be greater than 0.")

    @validates('total')
    def validate_total(self, value):
        """Validates that order total is greater than zero"""
        if value <= 0:
            raise ValidationError("Order total must be greater than 0.")

    @post_load
    def make_order(self, data):
        """creates a order object from data dictionary"""
        return Order(**data)
