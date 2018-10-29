from unittest.mock import patch
import pytest
from marshmallow import ValidationError
from appserver.service.products_service import ProductsService
import appserver.data.product_mapper
from appserver.service.exceptions import NotFoundError, ForbiddenError


def test_add_product_if_wrong_schema_raises_validation_error(product_data):
    with pytest.raises(ValidationError):
        ProductsService.add_product(product_data.invalid_product)


def test_add_product_if_no_product_sent_raises_validation_error():
    product_json = {}
    with pytest.raises(ValidationError):
        ProductsService.add_product(product_json)


@patch.object(appserver.data.product_mapper.ProductMapper, 'get_by_id')
def test_get_product_by_id_if_none_found_raises_not_found_error(pm_mock):
    pm_mock.return_value = None
    with pytest.raises(NotFoundError):
        ProductsService.get_product_by_id(15)


@patch.object(appserver.data.product_mapper.ProductMapper, 'get_many')
def test_get_products_if_none_found_raises_not_found_error(pm_mock):
    pm_mock.return_value = []
    with pytest.raises(NotFoundError):
        ProductsService.get_products()


@patch.object(appserver.data.product_mapper.ProductMapper, 'delete_one_by_id')
@patch.object(appserver.service.products_service.ProductsService, '_product_exists_and_belongs_to_user')
def test_delete_product_if_product_not_found_raises_not_found_error\
                (_product_exists_and_belongs_to_user_mock, delete_one_by_id_mock, user_data, product_data):
    _product_exists_and_belongs_to_user_mock.side_effect = NotFoundError("not found")
    delete_one_by_id_mock.return_value = False
    with pytest.raises(NotFoundError):
        ProductsService.delete_product(user_data.uid, product_data.product_id)


@patch.object(appserver.service.products_service.ProductsService, '_product_exists_and_belongs_to_user')
def test_delete_product_if_user_doesnt_own_product_raises_forbidden_error\
                (_product_exists_and_belongs_to_user_mock, user_data, product_data):
    _product_exists_and_belongs_to_user_mock.side_effect = ForbiddenError("forbidden")
    with pytest.raises(ForbiddenError):
        ProductsService.delete_product(user_data.uid, product_data.product_id)


@patch.object(appserver.data.product_mapper.ProductMapper, 'delete_one_by_id')
@patch.object(appserver.service.products_service.ProductsService, '_product_exists_and_belongs_to_user')
def test_delete_product(_product_exists_and_belongs_to_user_mock, delete_one_by_id_mock, user_data, product_data):
    _product_exists_and_belongs_to_user_mock.return_value = True
    delete_one_by_id_mock.return_value = True
    assert ProductsService.delete_product(user_data.uid, product_data.product_id)
