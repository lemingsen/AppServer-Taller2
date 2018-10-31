"""User models"""
from appserver.data.base_mapper import BaseMapper
from appserver.models.user import UserSchema


class UserMapper(BaseMapper):
    """User Model"""
    collection = 'users'
    schema = UserSchema()
