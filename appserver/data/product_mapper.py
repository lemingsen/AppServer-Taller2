"""product models"""
from bson.objectid import ObjectId
from appserver.models.product import ProductSchema
from appserver.data.base_mapper import BaseMapper


class ProductMapper(BaseMapper):
    """product models"""
    collection = 'products'
    schema = ProductSchema()

    @classmethod
    def add_question(cls, product_id, question):
        """Adds a question to the product's question list"""
        product = cls.find_one_and_update(
            {'_id': ObjectId(product_id)},
            {'$push': {'questions': question}}
        )
        return product

    @classmethod
    def add_answer(cls, product_id, question_id, answer):
        """Adds an answer to a question in the product's question list"""
        product = cls.find_one_and_update(
            {'_id': ObjectId(product_id), "questions.question_id": question_id},
            {'$push': {"questions.$.answers": answer}}
        )
        return product
