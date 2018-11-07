"""Category Model"""
from marshmallow import Schema, fields, post_load, validate
from appserver.utils.mongo import ObjectId
from appserver.models.base import BaseModel
# pylint: disable=R0903,R0201


class Category(BaseModel):
    """Category"""
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)


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
