"""User enpoints related tests"""
from unittest.mock import patch
import appserver.services.users_service


def test_endpoint_without_token_returns_401(client):
    response = client.get('/user/profile')
    assert response.status_code == 401


def test_register_if_body_is_not_json_returns_400_status(client, user_data):
    response = client.post('/user/register', data='Hola')
    assert response.status_code == 400


@patch.object(appserver.services.users_service.UserService, 'register')
def test_register_if_user_exists_returns_409_status(register_mock, client, user_data):
    register_mock.side_effect = appserver.services.exceptions.UserExistsError()
    response = client.post('/user/register', json=user_data.valid_user)
    assert response.status_code == 409


def test_register_if_invalid_user_returns_400_status(client, user_data):
    response = client.post('/user/register', json=user_data.invalid_user)
    assert response.status_code == 400


@patch.object(appserver.services.users_service.UserService, 'get_profile')
def test_get_profile_if_user_not_exists_returns_404_status(get_profile_mock, client, user_data):
    get_profile_mock.side_effect = appserver.services.exceptions.NotFoundError("User not found")
    response = client.get('/user/profile', headers=user_data.valid_token_header())
    assert response.status_code == 404


@patch.object(appserver.services.users_service.UserService, 'get_profile')
def test_get_profile_valid_token_returns_200_status(get_profile_mock, client, user_data):
    get_profile_mock.return_value = user_data.valid_user
    response = client.get('/user/profile', headers=user_data.valid_token_header())
    assert response.status_code == 200


def test_modify_profile_if_body_not_json_returns_400_status(client):
    pass
