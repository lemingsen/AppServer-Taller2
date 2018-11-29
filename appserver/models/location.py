"""Location models"""
from marshmallow import Schema, fields, post_load
# pylint: disable=R0903,R0201


class Location:
    """Location"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class LocationSchema(Schema):
    """Location marshmallow schema"""
    longitude = fields.Float(required=True)
    latitude = fields.Float(required=True)

    @post_load
    def make_location(self, data):
        """Deserializes data into a Location object"""
        return Location(**data)
