"""Order endpoints related tests"""
from unittest.mock import patch
import appserver.data.order_mapper
import appserver.models.product
import json


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
def test_new_order_if_not_enough_units_422_response(get_by_id_mock, client, order_data, product_data):
    product_with_3_units = product_data.get_product_with_3_units()
    order_with_9_units = order_data.input_order_with_9_units
    get_by_id_mock.return_value = product_with_3_units
    response = client.post('/orders',
                           headers=order_data.valid_token_header(),
                           data=json.dumps(order_with_9_units),
                           content_type='application/json')
    assert response.status_code == 422

