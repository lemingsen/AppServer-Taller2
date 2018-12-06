"""User models"""
from appserver.data.base_mapper import BaseMapper
from appserver.models.user import UserSchema


class UserMapper(BaseMapper):
    """User Model"""
    collection = 'users'
    schema = UserSchema()

    @classmethod
    def add_points(cls, uid, points):
        """Adds points to the user. In case points is negative it sustracts them."""
        return cls.find_one_and_update({'uid': uid}, {'$inc': {'points': points}})
