"""Product Model"""
from marshmallow import Schema, fields, post_load
from appserver.utils.mongo import ObjectId
from appserver.models.location import LocationSchema
from appserver.models.question import QuestionSchema
# pylint: disable=R0903,R0201


class Product:
    """Product"""
    def __init__(self, **kwargs):
        self.categories = []
        self.questions = []
        for key, value in kwargs.items():
            setattr(self, key, value)


class ProductSchema(Schema):
    """Product marshmallow schema"""
    _id = ObjectId()
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    seller = fields.Str(required=True)
    units = fields.Int(required=True)
    price = fields.Float(required=True)
    location = fields.Nested(LocationSchema, required=True)
    categories = fields.List(fields.Str())
    payment_methods = fields.List(fields.Str(), required=True)
    pictures = fields.List(fields.Url(), required=True)
    published = fields.Str()
    questions = fields.List(fields.Nested(QuestionSchema))

    @post_load
    def make_user(self, data):
        """Deserializes data into a Product object"""
        return Product(**data)
