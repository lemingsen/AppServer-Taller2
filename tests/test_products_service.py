from unittest.mock import patch
import pytest
from marshmallow import ValidationError
from appserver.service.products_service import ProductsService
import appserver.data.product_mapper
from appserver.service.exceptions import NotFoundError


def test_add_product_if_wrong_schema_raises_validation_error(product_data):
    with pytest.raises(ValidationError):
        ProductsService.add_product(product_data.invalid_product)


def test_add_product_if_no_product_sent_raises_validationerror():
    product_json = {}
    with pytest.raises(ValidationError):
        ProductsService.add_product(product_json)


@patch.object(appserver.data.product_mapper.ProductMapper, 'get_by_id')
def test_get_product_by_id_if_none_found_raises_notfounderror(pm_mock):
    pm_mock.return_value = None
    with pytest.raises(NotFoundError):
        ProductsService.get_product_by_id(15)


@patch.object(appserver.data.product_mapper.ProductMapper, 'get_many')
def test_get_products_if_none_found_raises_notfounderror(pm_mock):
    pm_mock.return_value = []
    with pytest.raises(NotFoundError):
        ProductsService.get_products()
