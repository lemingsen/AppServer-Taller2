"""Payment model"""
from marshmallow import Schema, fields, post_load, validate
# pylint: disable=R0903,R0201


class PaymentMethod:
    """Payment"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class PaymentMethodSchema(Schema):
    """marshmallow payment schema"""
    name = fields.Str(required=True, validate=validate.Length(
        min=1, error="Payment name cannot be empty"))
    type = fields.Int(required=True)
    image = fields.Url()

    @post_load
    def make_payment_method(self, data):
        """creates a Payment object from data dictionary"""
        return PaymentMethod(**data)
