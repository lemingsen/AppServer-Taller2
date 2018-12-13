"""Order endpoints related tests"""
from unittest.mock import patch
import appserver.data.order_mapper
from appserver.models.user import UserSchema
import appserver.services.shared_server_services
import appserver.services.user_scoring
import json
import flask_jwt_extended
import requests
from tests.conftest import ResponseSharedServerMock


def test_new_order_if_no_body_payload_returns_400_response(client, order_data):
    response = client.post('/orders',
                           headers=order_data.valid_token_header())
    assert response.status_code == 400


def test_new_order_if_body_is_not_json_400_response(client, order_data):
    response = client.post('/orders',
                           headers=order_data.valid_token_header(),
                           data=order_data.not_json(),
                           content_type='application/json')
    assert response.status_code == 400


@patch.object(appserver.data.product_mapper.ProductMapper, 'get_by_id')
def test_new_order_if_product_not_found_404_response(get_by_id_mock, client, order_data, product_data):
    get_by_id_mock.return_value = None
    response = client.post('/orders',
                           headers=order_data.valid_token_header(),
                           data=json.dumps(order_data.valid_input_order),
                           content_type='application/json')
    assert response.status_code == 404


@patch.object(appserver.data.product_mapper.ProductMapper, 'get_by_id')
@patch.object(appserver.data.user_mapper.UserMapper, 'get_one')
def test_new_order_if_not_enough_units_422_response(get_one_mock, get_by_id_mock, client, order_data, product_data, user_data):
    product_with_3_units = product_data.get_product_with_3_units()
    order_with_9_units = order_data.input_order_with_9_units
    get_by_id_mock.return_value = product_with_3_units
    user_schema = UserSchema()
    get_one_mock.return_value = user_schema.load(user_data.valid_user)
    response = client.post('/orders',
                           headers=order_data.valid_token_header(),
                           data=json.dumps(order_with_9_units),
                           content_type='application/json')
    assert response.status_code == 422


@patch.object(appserver.data.order_mapper.OrderMapper, 'get_many')
def test_get_sales_if_no_orders_returns_empty_list(get_many_mock, client, order_data):
    get_many_mock.return_value = []
    response = client.get('/orders/sales', headers=order_data.valid_token_header())
    body = response.get_json()
    assert body['count'] == 0


@patch.object(appserver.data.order_mapper.OrderMapper, 'get_many')
def test_get_purchases_if_no_orders_returns_empty_list(get_many_mock, client, order_data):
    get_many_mock.return_value = []
    response = client.get('/orders/purchases', headers=order_data.valid_token_header())
    body = response.get_json()
    assert body['count'] == 0


@patch.object(appserver.data.user_mapper.UserMapper, 'get_one')
@patch.object(appserver.data.product_mapper.ProductMapper, 'get_by_id')
@patch.object(appserver.services.shared_server_services.SharedServer, 'get_delivery_estimate')
def test_estimate_shipping_cost_if_delivery_cannot_be_done_returns_minus_one(get_delivery_estimate_mock, get_by_id_mock, user_mapper_get_one_mock, client, order_data, product_data, user_data):
    user_mapper_get_one_mock.return_value = user_data.get_valid_user()
    get_by_id_mock.return_value = product_data.valid_product
    get_delivery_estimate_mock.return_value = -1
    response = client.post('/orders/shipping/estimate',
                           headers=order_data.valid_token_header(),
                           data=json.dumps(order_data.estimate_shipping_input_data),
                           content_type='application/json')
    body = response.get_json()
    assert body['estimated_cost'] == -1


@patch.object(appserver.data.user_mapper.UserMapper, 'get_one')
@patch.object(appserver.data.product_mapper.ProductMapper, 'get_by_id')
@patch.object(appserver.services.shared_server_services.SharedServer, 'get_delivery_estimate')
def test_estimate_shipping_cost_if_delivery_can_be_done_returns_cost(get_delivery_estimate_mock, get_by_id_mock, user_mapper_get_one_mock, client, order_data, product_data, user_data):
    user_mapper_get_one_mock.return_value = user_data.get_valid_user()
    get_by_id_mock.return_value = product_data.valid_product
    shipping_cost = 45.43
    get_delivery_estimate_mock.return_value = shipping_cost
    response = client.post('/orders/shipping/estimate',
                           headers=order_data.valid_token_header(),
                           data=json.dumps(order_data.estimate_shipping_input_data),
                           content_type='application/json')
    body = response.get_json()
    assert body['estimated_cost'] == shipping_cost


@patch.object(flask_jwt_extended, 'get_jwt_identity')
@patch.object(appserver.data.order_mapper.OrderMapper, 'get_one')
def test_if_order_has_to_be_delivered_cannot_rate_if_not_delivered(order_find_one_mock, uid_mock, client, order_data):
    uid_mock.return_value = order_data.get_order_with_delivery_and_not_shipped().buyer
    order_find_one_mock.return_value = order_data.get_order_with_delivery_and_not_shipped()
    response = client.post('/orders/ratings/45',
                           headers=order_data.valid_token_header(),
                           data=json.dumps(order_data.positive_rating),
                           content_type='application/json')
    assert response.status_code == 403


@patch.object(flask_jwt_extended, 'get_jwt_identity')
@patch.object(appserver.data.order_mapper.OrderMapper, 'rate_purchase')
@patch.object(appserver.services.user_scoring.UserScoring, 'new_rating')
@patch.object(appserver.data.order_mapper.OrderMapper, 'get_one')
def test_if_order_has_to_be_delivered_can_rate_when_is_delivered(order_get_one_mock, user_scoring_new_rating_mock, order_mapper_rate_purchase_mock, uid_mock, client, order_data):
    uid_mock.return_value = order_data.get_order_with_delivery_and_shipped().buyer
    user_scoring_new_rating_mock.return_value = None
    order_mapper_rate_purchase_mock.return_value = None
    order_get_one_mock.return_value = order_data.get_order_with_delivery_and_shipped()
    response = client.post('/orders/ratings/45',
                           headers=order_data.valid_token_header(),
                           data=json.dumps(order_data.positive_rating),
                           content_type='application/json')
    assert response.status_code == 200


@patch.object(flask_jwt_extended, 'get_jwt_identity')
@patch.object(appserver.data.order_mapper.OrderMapper, 'get_one')
def test_if_order_has_not_to_be_delivered_cannot_rate_until_is_payed(order_get_one_mock, uid_mock, client, order_data):
    uid_mock.return_value = order_data.get_order_without_delivery_and_not_payed().buyer
    order_get_one_mock.return_value = order_data.get_order_without_delivery_and_not_payed()
    response = client.post('/orders/ratings/45',
                           headers=order_data.valid_token_header(),
                           data=json.dumps(order_data.positive_rating),
                           content_type='application/json')
    assert response.status_code == 403


@patch.object(flask_jwt_extended, 'get_jwt_identity')
@patch.object(appserver.data.order_mapper.OrderMapper, 'rate_purchase')
@patch.object(appserver.services.user_scoring.UserScoring, 'new_rating')
@patch.object(appserver.data.order_mapper.OrderMapper, 'get_one')
def test_if_order_has_not_to_be_delivered_can_rate_when_is_payed(order_get_one_mock, user_scoring_new_rating_mock, order_mapper_rate_purchase_mock, uid_mock, client, order_data):
    uid_mock.return_value = order_data.get_order_without_delivery_and_payed().buyer
    user_scoring_new_rating_mock.return_value = None
    order_mapper_rate_purchase_mock.return_value = None
    order_get_one_mock.return_value = order_data.get_order_without_delivery_and_payed()
    response = client.post('/orders/ratings/45',
                           headers=order_data.valid_token_header(),
                           data=json.dumps(order_data.positive_rating),
                           content_type='application/json')
    assert response.status_code == 200


@patch.object(appserver.data.order_mapper.OrderMapper, 'update_status')
@patch.object(requests, 'get')
@patch.object(flask_jwt_extended, 'get_jwt_identity')
@patch.object(appserver.data.order_mapper.OrderMapper, 'get_one')
def test_track_order_status_changes_from_compra_realizada_to_envio_realizado(order_mapper_get_one_mock, uid_mock, request_get_mock, order_mapper_update_status_mock, client, order_data):
    order_mapper_update_status_mock.return_value = None
    uid_mock.return_value = order_data.get_order_with_compra_realizada_status().buyer
    appserver.services.shared_server_services.SharedServer.auth_token = 'sadasdasd'
    request_get_mock.side_effect = [order_data.response_shared_server_pago_confirmado(), order_data.response_shared_server_envio_entregado()]
    order_mapper_get_one_mock.return_value = order_data.get_order_with_compra_realizada_status()

    response = client.get('/orders/tracking/45',
                          headers=order_data.valid_token_header())
    assert response.get_json()['status'] == 'ENVIO REALIZADO'
