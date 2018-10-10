"""User model"""
from marshmallow import Schema, fields
from models.model import Model


class UserSchema(Schema):
    """User marshmallow schema"""
    _id = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    uid = fields.Str(required=True)
    email = fields.Email()
    facebook = fields.Str()
    google = fields.Str()
    photo = fields.URL()
    member_since = fields.Str()
    last_login = fields.Str()


class User(Model):
    """User Model"""
    collection_name = 'users'
