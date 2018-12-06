"""Product Model"""
from marshmallow import Schema, fields, post_load, validates, ValidationError, validate
from appserver.utils.mongo import ObjectId
from appserver.models.location import LocationSchema
from appserver.models.question import QuestionSchema
from appserver.models.payment_method import PaymentMethodSchema
from appserver.models.base import BaseModel
# pylint: disable=R0903,R0201


class Product(BaseModel):
    """Product"""
    def __init__(self, **kwargs):
        super().__init__()
        self.categories = []
        self.questions = []
        self.payment_methods = []
        for key, value in kwargs.items():
            setattr(self, key, value)


class ProductSchema(Schema):
    """Product marshmallow schema"""
    _id = ObjectId()
    name = fields.Str()
    description = fields.Str()
    seller = fields.Str()
    units = fields.Int()
    price = fields.Float()
    location = fields.Nested(LocationSchema)
    categories = fields.List(fields.Str())
    payment_methods = fields.List(fields.Nested(PaymentMethodSchema))
    pictures = fields.List(fields.Url(), required=True)
    published = fields.Str()
    questions = fields.List(fields.Nested(QuestionSchema))
    distance = fields.Integer()
    points = fields.Integer()

    @post_load
    def make_user(self, data):
        """Deserializes data into a Product object"""
        return Product(**data)


class AddProductSchema(Schema):
    """Product marshmallow schema"""
    name = fields.Str(required=True, validate=validate.Length(
        min=1, error="Product name cannot be empty."))
    description = fields.Str(required=True, validate=validate.Length(
        min=1, error="Product description cannot be empty"))
    seller = fields.Str()
    units = fields.Int(required=True)
    price = fields.Float(required=True)
    location = fields.Nested(LocationSchema, required=True)
    categories = fields.List(fields.Str())
    payment_methods = fields.List(fields.Str(), required=True)
    pictures = fields.List(fields.Url(), required=True)
    published = fields.Str()
    questions = fields.List(fields.Nested(QuestionSchema))

    @validates('units')
    def validate_units(self, value):
        """Validates that product units are greater than zero"""
        if value <= 0:
            raise ValidationError("Product units must be greater than 0.")

    @validates('price')
    def validate_price(self, value):
        """Validates that product price is greater than zero"""
        if value <= 0:
            raise ValidationError("Product price must be greater than 0.")

    @validates('payment_methods')
    def validate_payment_methods(self, value):
        """Validates that there is at least one payment method available on product"""
        if not value:
            raise ValidationError("Must add at least one payment method.")

    @post_load
    def make_user(self, data):
        """Deserializes data into a Product object"""
        return Product(**data)
