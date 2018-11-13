"""User Model"""
from marshmallow import Schema, fields, post_load, validate
from appserver.utils.mongo import ObjectId
from appserver.models.base import BaseModel
# pylint: disable=R0903,R0201


class User(BaseModel):
    """User"""
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)


class UserSchema(Schema):
    """User marshmallow schema"""
    _id = ObjectId()
    name = fields.Str(validate=validate.Length(
        min=1, error="User name cannot be empty."))
    surname = fields.Str(validate=validate.Length(
        min=1, error="User surname cannot be empty."))
    uid = fields.Str(required=True)
    email = fields.Email(required=True)
    facebook = fields.Str()
    google = fields.Str()
    photo = fields.URL()
    member_since = fields.Str()
    last_login = fields.Str()

    @post_load
    def make_user(self, data):
        """Deserializes data into a User object"""
        return User(**data)
