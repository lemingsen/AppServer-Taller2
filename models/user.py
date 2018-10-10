from models.model import Model
from marshmallow import Schema, fields


class UserSchema(Schema):
    _id = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    uid = fields.Str(required=True)
    email = fields.Email()
    facebook = fields.Str()
    google = fields.Str()
    photo = fields.URL()
    member_since = fields.DateTime(format="rfc")
    last_login = fields.DateTime(format="rfc")


class User(Model):
    collection_name = 'users'
