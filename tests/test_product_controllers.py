"""Product endpoints related tests"""
from unittest.mock import patch
import json
import appserver.services.product_services
import appserver.data.product_mapper
import appserver.data.category_mapper
from appserver.services.exceptions import NotFoundError


def test_get_products_without_token_returns_401_response(client):
    response = client.get('/products')
    assert response.status_code == 401


def test_get_products_with_invalid_token_returns_422_response(client, product_data):
    response = client.get('/products',
                          headers=product_data.invalid_token_header())
    assert response.status_code == 422


@patch.object(appserver.services.product_services.ProductsService, 'get_products')
def test_get_products_with_token_returns_200_response(get_products_mock, client, product_data):

    get_products_mock.return_value = product_data.get_products_return_value()
    response = client.get('/products',
                          headers=product_data.valid_token_header())
    assert response.status_code == 200


def test_get_product_without_token_returns_401_response(client):
    response = client.get('/products/512')
    assert response.status_code == 401


def test_add_product_without_token_returns_401_response(client):
    response = client.post('/products')
    assert response.status_code == 401


def test_add_product_if_body_not_json_400_response(client, product_data):
    response = client.post('/products',
                           headers=product_data.valid_token_header())
    assert response.status_code == 400


def test_delete_product_without_token_401_response(client, product_data):
    response = client.delete('/products/5bbe37a3c00f593839d19e')
    assert response.status_code == 401


@patch.object(appserver.services.product_services.ProductsService, '_check_product_exists_and_belongs_to_user')
def test_delete_product_if_not_found_404_response(_product_exists_and_belongs_to_user_mock, client, user_data, product_data):
    _product_exists_and_belongs_to_user_mock.side_effect = NotFoundError("Product does not exist.")
    response = client.delete('/products/5bbe37a1e3c00f593839d19e',
                             headers=product_data.valid_token_header())
    assert response.status_code == 404


def test_delete_product_if_invalid_product_id_400_response(client, user_data, product_data):
    response = client.delete('/products/5bbe37a3c00f593839d19e',
                             headers=product_data.valid_token_header())
    assert response.status_code == 400


@patch.object(appserver.data.product_mapper.ProductMapper, 'get_by_id')
def test_delete_product_if_user_does_not_own_product_403_response(get_by_id_mock, client, user_data, product_data):
    get_by_id_mock.return_value = product_data.get_valid_product_from_other_user_than_valid_token_header()
    response = client.delete('/products/5bbe37a3c00f593839d19e',
                             headers=product_data.valid_token_header())
    assert response.status_code == 403


@patch.object(appserver.data.product_mapper.ProductMapper, 'find_one_and_update')
def test_add_question_if_product_does_not_exist_404_response(find_one_and_update_mock, client, product_data):
    find_one_and_update_mock.return_value = None
    response = client.post('products/5bbe37a1e3c00f593839d19e/questions',
                           headers=product_data.valid_token_header(),
                           data=json.dumps(product_data.valid_question),
                           content_type='application/json')
    assert response.status_code == 404


def test_add_question_if_invalid_parameters_in_body_400_response(client, product_data):
    response = client.post('products/5bbe37a1e3c00f593839d19e/questions',
                           headers=product_data.valid_token_header(),
                           data=json.dumps(product_data.invalid_question),
                           content_type='application/json')
    assert response.status_code == 400


@patch.object(appserver.data.product_mapper.ProductMapper, 'find_one_and_update')
def test_add_answer_if_product_does_not_exist_404_response(find_one_and_update_mock, client, product_data):
    find_one_and_update_mock.return_value = None
    response = client.post('products/5bbe37a1e3c00f593839d19e/questions/5bbe36a1e3c00f593839d19e/answers',
                           headers=product_data.valid_token_header(),
                           data=json.dumps(product_data.valid_answer),
                           content_type='application/json')
    assert response.status_code == 404


@patch.object(appserver.data.product_mapper.ProductMapper, 'find_one_and_update')
def test_add_answer_if_question_does_not_exist_404_response(find_one_and_update_mock, client, product_data):
    find_one_and_update_mock.return_value = None
    response = client.post('products/5bbe37a1e3c00f593839d19e/questions/5bbe36a1e3c00f593839d19e/answers',
                           headers=product_data.valid_token_header(),
                           data=json.dumps(product_data.valid_answer),
                           content_type='application/json')
    assert response.status_code == 404


def test_add_answer_if_invalid_parameters_in_body_400_response(client, product_data):
    response = client.post('products/5bbe37a1e3c00f593839d19e/questions/5bbe36a1e3c00f593839d19e/answers',
                           headers=product_data.valid_token_header(),
                           data=json.dumps(product_data.invalid_answer),
                           content_type='application/json')
    assert response.status_code == 400


def test_add_category_if_invalid_schema_400_response(client, product_data):
    response = client.post('products/categories',
                           headers=product_data.valid_token_header(),
                           data=json.dumps(product_data.invalid_input_category),
                           content_type='application/json')
    assert response.status_code == 400


def test_add_category_if_empty_category_400_response(client, product_data):
    response = client.post('products/categories',
                           headers=product_data.valid_token_header(),
                           data=json.dumps(product_data.empty_input_category),
                           content_type='application/json')
    assert response.status_code == 400


@patch.object(appserver.data.category_mapper.CategoryMapper, 'exists')
def test_add_category_if_category_exists_409_response(exists_mock, client, product_data):
    exists_mock.return_value = True
    response = client.post('products/categories',
                           headers=product_data.valid_token_header(),
                           data=json.dumps(product_data.valid_input_category),
                           content_type='application/json')
    assert response.status_code == 409


@patch.object(appserver.data.category_mapper.CategoryMapper, 'exists')
def test_modify_category_if_category_exists_409_response(exists_mock, client, product_data):
    exists_mock.return_value = True
    response = client.put('products/categories/5be08844e3c00c20b1377151',
                          headers=product_data.valid_token_header(),
                          data=json.dumps(product_data.valid_input_category),
                          content_type='application/json')
    assert response.status_code == 409


def test_modify_category_if_empty_category_400_response(client, product_data):
    response = client.put('products/categories/5be08844e3c00c20b1377151',
                          headers=product_data.valid_token_header(),
                          data=json.dumps(product_data.empty_input_category),
                          content_type='application/json')
    assert response.status_code == 400


@patch.object(appserver.data.category_mapper.CategoryMapper, 'delete_one_by_id')
def test_delete_category_if_category_not_found_404_response(delete_one_by_id_mock, client, product_data):
    delete_one_by_id_mock.return_value = False
    response = client.delete('products/categories/5be08844e3c00c20b1377151',
                             headers=product_data.valid_token_header(),
                             data=json.dumps(product_data.empty_input_category),
                             content_type='application/json')
    assert response.status_code == 404







