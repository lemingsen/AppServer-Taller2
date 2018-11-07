"""Product Model"""
from marshmallow import Schema, fields, post_load, validates, ValidationError
from appserver.utils.mongo import ObjectId
from appserver.models.location import LocationSchema
from appserver.models.question import QuestionSchema
# pylint: disable=R0903,R0201,C0103


class Product:
    """Product"""
    def __init__(self, **kwargs):
        self._id = None
        self.categories = []
        self.questions = []
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def id(self):
        """Product id property"""
        return self._id
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

    @validates('units')
    def validate_units(self, value):
        """Validates that product units are greater than zero"""
        if value <= 0:
            raise ValidationError("Product units must be greater than 0.")

    @validates('price')
    def validate_price(self, value):
        """Validates that product price is greater than zero"""
        if value <= 0:
            raise ValidationError("Product price must be greater than 0.")

    @post_load
    def make_user(self, data):
        """Deserializes data into a Product object"""
        return Product(**data)
