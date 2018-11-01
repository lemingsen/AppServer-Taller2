from unittest.mock import patch
import pytest
from marshmallow import ValidationError
from appserver.services.user_services import UserService
import appserver.data.user_mapper
import appserver.utils.firebase
from appserver.services.exceptions import NotFoundError, UserExistsError


@patch.object(appserver.data.user_mapper.UserMapper, 'find_one_and_update')
@patch.object(appserver.utils.firebase.Firebase, 'decode_token')
def test_login_if_user_not_found_raises_not_found_error(firebase_mock, um_mock, user_data):
    firebase_mock.return_value = user_data.valid_user
    um_mock.return_value = None
    with pytest.raises(NotFoundError):
        UserService.login(user_data.valid_token)


def test_modify_profile_if_wrong_schema_raises_validation_error():
    pass


@patch.object(appserver.services.user_services.UserService, '_user_exists')
def test_register_if_user_exists_raises_user_exists_error(user_exists_mock, user_data):
    user_exists_mock.return_value = True
    with pytest.raises(UserExistsError):
        UserService.register(user_data.valid_user)


def test_register_if_wrong_schema_raises_validation_error(user_data):
    with pytest.raises(ValidationError):
        UserService.register(user_data.invalid_user)


@patch.object(appserver.data.user_mapper.UserMapper, 'get_one')
def test_get_profile_if_not_found_raises_not_found_error(get_one_mock, user_data):
    get_one_mock.return_value = None
    with pytest.raises(NotFoundError):
        UserService.get_profile(user_data.uid)
