"""User enpoints related tests"""


def test_endpoint_without_token_raises_401(client):
    response = client.get('/user/profile')
    assert response.status_code == 401


def test_login_if_firebase_token_invalid_raises_value_error(client):
    pass


def test_register_if_body_is_not_json_raises_400(client):
    pass


def test_register_if_user_exists_raises_409(client):
    pass


def test_register_if_required_fields_not_in_body_raises_validationerror(client):
    pass


def test_get_profile_if_user_not_exists_raises_404(client):
    pass


def test_modify_profile_if_body_not_json_raises_400(client):
    pass


