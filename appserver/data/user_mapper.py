"""User model"""
from appserver.data.base_mapper import BaseMapper
from appserver.model.user import UserSchema


class UserMapper(BaseMapper):
    """User Model"""
    collection = 'users'
    schema = UserSchema()
