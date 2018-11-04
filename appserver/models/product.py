"""Product Model"""
from marshmallow import Schema, fields, post_load
from appserver.utils.mongo import ObjectId
from appserver.models.location import LocationSchema
from appserver.models.question import QuestionSchema
# pylint: disable=R0903,R0201


class Product():
    """Product"""
    def __init__(self, **kwargs):
        self.categories = []
        self.questions = []
        for key, value in kwargs.items():
            setattr(self, key, value)

    # def add_question(self, question):
    #     self.questions.append(question)
    #
    # def add_answer(self, answer):
    #     ret = False
    #     for question in self.questions:
    #         if question.question_id == answer.question_id:
    #             question.answers.append(answer)
    #             ret = True
    #             break
    #     return ret
    #
    # def buy(self, quantity, buyer_id):
    #     if quantity > self.units:
    #         return None


class ProductSchema(Schema):
    """Product marshmallow schema"""
    _id = ObjectId()
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    seller = fields.Str(required=True)
    units = fields.Int(required=True)
    price = fields.Float(required=True)
    location = fields.Nested(LocationSchema, required=True)
    categories = fields.List(fields.Str())
    payment_methods = fields.List(fields.Str(), required=True)
    pictures = fields.List(fields.Url(), required=True)
    published = fields.Str()
    questions = fields.List(fields.Nested(QuestionSchema))

    @post_load
    def make_user(self, data):
        """Deserializes data into a Product object"""
        return Product(**data)
