"""User Model"""
from datetime import datetime
from marshmallow import Schema, fields, post_load, validate
from appserver.utils.mongo import ObjectId
from appserver.models.base import BaseModel
from appserver.models.location import LocationSchema
# pylint: disable=R0903,R0201,E1101,W0201


class UserMetadata:
    """UserMetadata"""
    def __init__(self, **kwargs):
        self.publications = 0
        self.purchases = 0
        self.sales = 0
        self.positive_ratings = 0
        self.neutral_ratings = 0
        self.negative_ratings = 0
        self.points_log = []
        for key, value in kwargs.items():
            setattr(self, key, value)


class UserMetadataSchema(Schema):
    """UserMetadataSchema"""
    publications = fields.Int(required=True)
    purchases = fields.Int(required=True)
    sales = fields.Int(required=True)
    positive_ratings = fields.Int(required=True)
    neutral_ratings = fields.Int(required=True)
    negative_ratings = fields.Int(required=True)
    points_log = fields.List(fields.Str(), required=True)

    @post_load
    def make_user_metadata(self, data):
        """Deserializes data into a UserMetadata object"""
        return UserMetadata(**data)


class User(BaseModel):
    """User"""
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def username(self):
        """Returns name + surname"""
        return self.name + " " + self.surname

    def register_init(self):
        """Sets variables for registering user"""
        self.member_since = str(datetime.now())
        self.last_login = self.member_since
        self.points = 0
        self.metadata = UserMetadata()


class UserSchema(Schema):
    """User marshmallow schema"""
    _id = ObjectId()
    name = fields.Str(required=True, validate=validate.Length(
        min=1, error="User name cannot be empty."))
    surname = fields.Str(required=True, validate=validate.Length(
        min=1, error="User surname cannot be empty."))
    uid = fields.Str(required=True)
    location = fields.Nested(LocationSchema, required=True)
    email = fields.Email(required=True)
    facebook = fields.Str()
    google = fields.Str()
    photo = fields.URL()
    member_since = fields.Str()
    last_login = fields.Str()
    points = fields.Int()
    purchases = fields.Int()
    metadata = fields.Nested(UserMetadataSchema)

    @post_load
    def make_user(self, data):
        """Deserializes data into a User object"""
        return User(**data)
