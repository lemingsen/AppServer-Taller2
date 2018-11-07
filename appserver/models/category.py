"""Category Model"""
from marshmallow import Schema, fields, post_load, validate
from appserver.utils.mongo import ObjectId
# pylint: disable=R0903,R0201


class Category:
    """Category"""
    def __init__(self, **kwargs):
        self._id = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def id(self):
        return self._id


class CategorySchema(Schema):
    """Category marshmallow schema"""
    _id = ObjectId()
    name = fields.Str(required=True, validate=validate.Length(
        min=1, error="Product category cannot be empty."))
    image = fields.Url()

    @post_load
    def make_category(self, data):
        """Deserializes data into a Category object"""
        return Category(**data)
