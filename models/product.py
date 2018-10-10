from models.model import Model
from marshmallow import Schema, fields


class LocationSchema(Schema):
    x = fields.Float(required=True)
    y = fields.Float(required=True)


class ProductSchema(Schema):
    _id = fields.Str()
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    seller = fields.Str(required=True)
    units = fields.Int(required=True)
    price = fields.Float(required=True)
    location = fields.Nested(LocationSchema, required=True)
    categories = fields.List(fields.Str())
    payment_methods = fields.List(fields.Str(), required=True)
    pictures = fields.List(fields.Url(), required=True)
    published = fields.Str(required=True)


class Product(Model):
    collection_name = 'products'
