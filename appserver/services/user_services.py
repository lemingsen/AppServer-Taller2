"""User services"""
from datetime import datetime
import os
import json
from flask_jwt_extended import create_access_token
from appserver.services.exceptions import NotFoundError, DataExistsError
from appserver.utils.firebase import Firebase
from appserver.data.user_mapper import UserMapper
from appserver.models.user import UserSchema


class UserService:
    """User Services"""
    schema = UserSchema()

    @classmethod
    def login(cls, firebase_token):
        """Login services: returns a server access token after authenticating with firebase_token"""
        firebase = Firebase(json.loads(os.environ['FIREBASE_CONFIG']))
        uid = firebase.decode_token(firebase_token)
        user = UserMapper.find_one_and_update\
            ({'uid': uid}, {'$set': {'last_login': str(datetime.now())}})
        if user is None:
            raise NotFoundError("User not found.")
        access_token = create_access_token(identity=uid, fresh=True, expires_delta=False)
        return access_token

    @classmethod
    def register(cls, data):
        """Register services: registers a user with data passed in data dictionary. Returns
        the user id of the new user"""
        user = cls.schema.load(data)
        if UserMapper.exists({'uid': user.uid}):
            raise DataExistsError("User exists.")
        user.member_since = str(datetime.now())
        user.last_login = user.member_since
        uid = UserMapper.insert(cls.schema.load(data))
        return uid

    @classmethod
    def get_profile(cls, uid):
        """Get profile services: returns user profile of user with user id uid"""
        user = UserMapper.get_one({"uid": uid})
        if user is None:
            raise NotFoundError("User not found.")
        return cls.schema.dump(user)

    @classmethod
    def modify_profile(cls, uid, user):
        """Modify profile services: returns"""
        user = UserMapper.modify({"uid": uid}, cls.schema.load(user))
        return cls.schema.dump(user)

