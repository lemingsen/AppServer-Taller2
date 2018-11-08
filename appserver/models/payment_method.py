"""Payment model"""
from marshmallow import Schema, fields, post_load, validate
from appserver.utils.mongo import ObjectId
from appserver.models.base import BaseModel
# pylint: disable=R0903,R0201


class PaymentMethod(BaseModel):
    """Payment"""
    def __init__(self, **kwargs):
        super().__init__()
        self.name = None
        self.image = None
        self.fields = []
        for key, value in kwargs.items():
            setattr(self, key, value)


class PaymentMethodField:
    """Payment Field"""
    def __init__(self, **kwargs):
        self.name = None
        self.value = None
        self.validation = None
        for key, value in kwargs.items():
            setattr(self, key, value)


class PaymentMethodFieldSchema(Schema):
    """marshmallow payment field schema"""
    name = fields.Str(required=True, validate=validate.Length(
        min=1, error="Payment field name cannot be empty"))
    value = fields.Str(required=True, validate=validate.Length(
        min=1, error="Payment value field cannot be empty"))
    validation = fields.Str()

    @post_load
    def make_payment_method_field(self, data):
        """creates a PaymentField object from data dictionary"""
        return PaymentMethodField(**data)


class PaymentMethodSchema(Schema):
    """marshmallow payment schema"""
    _id = ObjectId()
    name = fields.Str(required=True, validate=validate.Length(
        min=1, error="Payment name cannot be empty"))
    image = fields.Url()
    fields = fields.List(fields.Nested(PaymentMethodFieldSchema))

    @post_load
    def make_payment_method(self, data):
        """creates a Payment object from data dictionary"""
        return PaymentMethod(**data)
