"""Question models"""
from marshmallow import Schema, fields, post_load
from appserver.utils.mongo import ObjectId
from appserver.models.answer import AnswerSchema
# pylint: disable=R0903,R0201


class Question:
    """Question"""
    def __init__(self, **kwargs):
        self.answers = []
        for key, value in kwargs.items():
            setattr(self, key, value)


class QuestionSchema(Schema):
    """Marshmallow question schema"""
    question_id = ObjectId()
    datetime = fields.Str()
    question = fields.Str(required=True)
    uid = fields.Str()
    answers = fields.List(fields.Nested(AnswerSchema))

    @post_load
    def make_question(self, data):
        """Deserializes data into a Question object"""
        return Question(**data)
