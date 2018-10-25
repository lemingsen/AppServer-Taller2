"""User Model"""
from marshmallow import Schema, fields, post_load
from appserver.utils.mongo import ObjectId
# pylint: disable=R0903,R0201


class User:
    """User"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class UserSchema(Schema):
    """User marshmallow schema"""
    _id = ObjectId()
    name = fields.Str()
    surname = fields.Str()
    uid = fields.Str(required=True)
    email = fields.Email()
    facebook = fields.Str()
    google = fields.Str()
    photo = fields.URL()
    member_since = fields.Str()
    last_login = fields.Str()

    @post_load
    def make_user(self, data):
        """Deserializes data into a User object"""
        return User(**data)
