from unittest.mock import patch
import pytest
from marshmallow import ValidationError
from appserver.services.product_services import ProductsService
import appserver.data.product_mapper
import appserver.data.category_mapper
from appserver.services.exceptions import NotFoundError, ForbiddenError, DataExistsError


def test_add_product_if_wrong_schema_raises_validation_error(product_data, user_data):
    with pytest.raises(ValidationError):
        ProductsService.add_product(product_data.invalid_product, user_data.uid)


def test_add_product_if_no_product_sent_raises_validation_error(user_data):
    product_json = {}
    with pytest.raises(ValidationError):
        ProductsService.add_product(product_json, user_data.uid)


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
@patch.object(appserver.services.product_services.ProductsService, '_product_exists_and_belongs_to_user')
def test_delete_product_if_product_not_found_raises_not_found_error(
        _product_exists_and_belongs_to_user_mock,
        delete_one_by_id_mock, user_data, product_data):
    _product_exists_and_belongs_to_user_mock.side_effect = NotFoundError("not found")
    delete_one_by_id_mock.return_value = False
    with pytest.raises(NotFoundError):
        ProductsService.delete_product(user_data.uid, product_data.product_id)


@patch.object(appserver.services.product_services.ProductsService, '_product_exists_and_belongs_to_user')
def test_delete_product_if_user_doesnt_own_product_raises_forbidden_error\
                (_product_exists_and_belongs_to_user_mock, user_data, product_data):
    _product_exists_and_belongs_to_user_mock.side_effect = ForbiddenError("forbidden")
    with pytest.raises(ForbiddenError):
        ProductsService.delete_product(user_data.uid, product_data.product_id)


@patch.object(appserver.data.product_mapper.ProductMapper, 'delete_one_by_id')
@patch.object(appserver.services.product_services.ProductsService, '_product_exists_and_belongs_to_user')
def test_delete_product(_product_exists_and_belongs_to_user_mock,
                        delete_one_by_id_mock, user_data, product_data):
    _product_exists_and_belongs_to_user_mock.return_value = True
    delete_one_by_id_mock.return_value = True
    assert ProductsService.delete_product(user_data.uid, product_data.product_id)


@patch.object(appserver.data.product_mapper.ProductMapper, 'find_one_and_update')
def test_add_question_if_product_not_found_raises_not_found_error(find_one_and_update_mock, product_data, user_data):
    find_one_and_update_mock.return_value = None
    with pytest.raises(NotFoundError):
        ProductsService.add_question(product_data.valid_question, product_data.product_id, user_data.uid)


def test_add_question_if_not_valid_question_raises_validation_error(product_data, user_data):
    with pytest.raises(ValidationError):
        ProductsService.add_question(product_data.invalid_question, product_data.product_id, user_data.uid)


@patch.object(appserver.data.product_mapper.ProductMapper, 'find_one_and_update')
def test_add_answer_if_product_not_found_raises_not_found_error(find_one_and_update_mock, product_data, user_data):
    find_one_and_update_mock.return_value = None
    with pytest.raises(NotFoundError):
        ProductsService.add_answer(product_data.valid_answer, product_data.product_id,
                                   product_data.question_id, user_data.uid)


def test_add_answer_if_not_valid_answer_raises_validation_error(product_data, user_data):
    with pytest.raises(ValidationError):
        ProductsService.add_answer(product_data.invalid_answer, product_data.product_id,
                                   product_data.question_id, user_data.uid)


@patch.object(appserver.data.category_mapper.CategoryMapper, 'exists')
def test_add_category_if_category_exists_raises_data_exists_error(exists_mock, product_data):
    exists_mock.return_value = True
    with pytest.raises(DataExistsError):
        ProductsService.add_category(product_data.valid_input_category)


@patch.object(appserver.data.category_mapper.CategoryMapper, 'exists')
def test_modify_category_if_category_name_exists_raises_data_exists_error(exists_mock, product_data):
    exists_mock.return_value = True
    with pytest.raises(DataExistsError):
        ProductsService.modify_category(product_data.category_id, product_data.valid_input_category)


@patch.object(appserver.data.category_mapper.CategoryMapper, 'exists')
@patch.object(appserver.data.category_mapper.CategoryMapper, 'modify')
def test_modify_category_if_category_not_found_raises_not_found_error(modify_mock, exists_mock, product_data):
    exists_mock.return_value = False
    modify_mock.return_value = None
    with pytest.raises(NotFoundError):
        ProductsService.modify_category(product_data.category_id, product_data.valid_input_category)


@patch.object(appserver.data.category_mapper.CategoryMapper, 'delete_one_by_id')
def test_delete_category_if_category_not_found_raises_not_found_error(exists_mock, product_data):
    exists_mock.return_value = False
    with pytest.raises(NotFoundError):
        ProductsService.delete_category(product_data.category_id)
