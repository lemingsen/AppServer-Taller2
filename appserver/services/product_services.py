"""Product Services"""
from datetime import datetime
import bson
from appserver.models.product import ProductSchema
from appserver.models.question import QuestionSchema
from appserver.models.answer import AnswerSchema
from appserver.models.category import CategorySchema
from appserver.models.product import AddProductSchema
from appserver.data.product_mapper import ProductMapper
from appserver.data.category_mapper import CategoryMapper
from appserver.data.payment_method_mapper import PaymentMethodMapper
from appserver.services.exceptions import NotFoundError, ForbiddenError, DataExistsError
from appserver.models.query import ProductsQuerySchema


class ProductsService:
    """Product Services"""
    schema = ProductSchema()

    @classmethod
    def add_product(cls, product_json, uid):
        """Add product services:"""
        product_json['seller'] = uid
        add_product_schema = AddProductSchema()
        product = add_product_schema.load(product_json)
        aux = []
        for payment_method_name in product.payment_methods:
            payment_method = PaymentMethodMapper.get_one({'name': payment_method_name})
            if payment_method is None:
                raise NotFoundError(payment_method_name + " payment method is not available.")
            aux.append(payment_method)
        product.payment_methods = aux
        product.published = str(datetime.now())
        return ProductMapper.insert(product)

    @classmethod
    def get_product_by_id(cls, product_id):
        """Get product by id services:"""
        product = ProductMapper.get_by_id(product_id)
        if product is None:
            raise NotFoundError("Product not found.")
        return cls.schema.dump(product)

    @classmethod
    def get_products(cls, filters=None):
        """Get products services: returns all the
         products that match with filters parameters"""

        query = None
        if filters is not None:
            products_query_schema = ProductsQuerySchema()
            query_builder = products_query_schema.load(filters)
            query = query_builder.get_query()
        products = ProductMapper.get_many(query)
        if not products:
            raise NotFoundError("No product matches the query.")
        ret = []
        for product in products:
            ret.append(cls.schema.dump(product))
        return ret

    @classmethod
    def delete_product(cls, uid, product_id):
        """Delete product services: deletes product product_id from user uid."""
        cls._check_product_exists_and_belongs_to_user(uid, product_id)
        if not ProductMapper.delete_one_by_id(product_id):
            raise NotFoundError("Product not found.")
        return True

    @classmethod
    def add_question(cls, question_dict, product_id, uid):
        """Add question services: adds a question by the user with id uid to the product
        with id product_id. Returns the product with the added question."""
        question_schema = QuestionSchema()
        question = question_schema.load(question_dict)
        question.id = bson.ObjectId()
        question.uid = uid
        question.datetime = str(datetime.now())
        product = ProductMapper.find_one_and_update(
            {'_id': bson.ObjectId(product_id)},
            {'$push': {'questions': question_schema.dump(question)}}
        )
        if product is None:
            raise NotFoundError("Product not found.")
        return cls.schema.dump(product)

    @classmethod
    def add_answer(cls, answer_dict, product_id, question_id, uid):
        """Add answer services: adds an answer to question_id question in
         product_id product"""
        answer_schema = AnswerSchema()
        answer = answer_schema.load(answer_dict)
        cls._check_product_exists_and_belongs_to_user(uid, product_id)
        answer.id = bson.ObjectId()
        answer.uid = uid
        answer.datetime = str(datetime.now())
        product = ProductMapper.find_one_and_update(
            {'_id': bson.ObjectId(product_id), "questions._id": question_id},
            {'$set': {"questions.$.answer": answer_schema.dump(answer)}}
        )
        if product is None:
            raise NotFoundError("Product not found.")
        return cls.schema.dump(product)

    @classmethod
    def get_categories(cls):
        """Returns available product categories"""
        category_schema = CategorySchema()
        categories = CategoryMapper.get_many()
        ret = []
        for category in categories:
            ret.append(category_schema.dump(category))
        return ret

    @classmethod
    def add_category(cls, category_dict):
        """Adds a product category"""
        category_schema = CategorySchema()
        category = category_schema.load(category_dict)
        if CategoryMapper.exists({'name': category.name}):
            raise DataExistsError("Product category already exists.")
        return CategoryMapper.insert(category_schema.dump(category))

    @classmethod
    def modify_category(cls, category_id, category_dict):
        """Modifies a product category"""
        category_schema = CategorySchema()
        category = category_schema.load(category_dict)
        if CategoryMapper.exists(
                {'_id': {'$ne': bson.ObjectId(category_id)},
                 'name': category.name}):
            raise DataExistsError("Product category already exists.")
        ret = CategoryMapper.modify({"_id": bson.ObjectId(category_id)}, category)
        if ret is None:
            raise NotFoundError("Category does not exist.")
        return ret

    @classmethod
    def delete_category(cls, category_id):
        """Deletes a product category"""
        if not CategoryMapper.delete_one_by_id(category_id):
            raise NotFoundError("Category not found.")

    @classmethod
    def _check_product_exists_and_belongs_to_user(cls, uid, product_id):
        """Checks if product exists and belongs to user."""
        product = ProductMapper.get_by_id(product_id)
        if product is None:
            raise NotFoundError("Product does not exist.")
        if product.seller != uid:
            raise ForbiddenError("User can only delete his own products")
        return True
