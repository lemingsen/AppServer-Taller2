"""Order Services tests"""
from unittest.mock import patch
import appserver.data.order_mapper
from appserver.services.order_services import OrderServices
from appserver.services.exceptions import NotFoundError, NotEnoughUnitsError
import appserver.models.product
from marshmallow.exceptions import ValidationError
import pytest


@patch.object(appserver.data.product_mapper.ProductMapper, 'get_by_id')
def test_new_order_if_product_not_found_raises_not_found_error(get_by_id_mock, order_data, user_data):
    get_by_id_mock.return_value = None
    with pytest.raises(NotFoundError):
        OrderServices.new_order(user_data.valid_user, order_data.valid_input_order)


def test_new_order_if_order_data_invalid_schema_raises_validation_error(order_data, user_data):
    with pytest.raises(ValidationError):
        OrderServices.new_order(user_data.valid_user, order_data.invalid_input_order)


def test_new_order_if_order_units_are_negative_raises_validation_error(order_data, user_data):
    with pytest.raises(ValidationError):
        OrderServices.new_order(user_data.valid_user, order_data.negative_units_input_order)


@patch.object(appserver.data.product_mapper.ProductMapper, 'get_by_id')
def test_new_order_if_order_units_greater_than_product_units_raises_not_enough_units_error(
        get_by_id_mock, order_data, user_data, product_data):
    product_with_3_units = product_data.get_product_with_3_units()
    get_by_id_mock.return_value = product_with_3_units
    with pytest.raises(NotEnoughUnitsError):
        OrderServices.new_order(user_data.valid_user, order_data.input_order_with_9_units)


