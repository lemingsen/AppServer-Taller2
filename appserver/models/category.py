"""Category Model"""
from marshmallow import Schema, fields, post_load
from appserver.utils.mongo import ObjectId
# pylint: disable=R0903,R0201


class Category:
    """Category"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class CategorySchema(Schema):
    """Category marshmallow schema"""
    _id = ObjectId()
    name = fields.Str(required=True)
    image = fields.Url()

    @post_load
    def make_category(self, data):
        """Deserializes data into a Category object"""
        return Category(**data)
