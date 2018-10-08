from models.model import Model
from marshmallow import Schema, fields, post_load


class UserSchema(Schema):
    name = fields.Str()
    surname = fields.Str()
    uid = fields.Str()
    email = fields.Email()
    facebook = fields.Str()
    google = fields.Str()
    photo = fields.URL()
    member_since = fields.DateTime()
    last_login = fields.DateTime()

    # @post_load
    # def make_user(data):
    #     return User(**data)


class User(Model):
    collection_name = 'users'
