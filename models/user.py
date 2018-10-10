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
    member_since = fields.Str()
    last_login = fields.Str()


class User(Model):
    collection_name = 'users'
