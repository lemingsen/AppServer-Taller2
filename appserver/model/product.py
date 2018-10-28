"""Product Model"""
from marshmallow import Schema, fields, post_load
from appserver.utils.mongo import ObjectId
# pylint: disable=R0903,R0201


class Location:
    """Location"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Product:
    """Product"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # if key == 'location':
            #     self.location = Location(**value)
            setattr(self, key, value)


class LocationSchema(Schema):
    """Location marshmallow schema"""
    x = fields.Float(required=True)
    y = fields.Float(required=True)

    @post_load
    def make_location(self, data):
        """Deserializes data into a Location object"""
        return Location(**data)


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

    @post_load
    def make_user(self, data):
        """Deserializes data into a Product object"""
        return Product(**data)
