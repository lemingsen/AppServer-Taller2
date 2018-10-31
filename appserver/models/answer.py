"""Answer models"""
from marshmallow import Schema, fields, post_load
# pylint: disable=R0903,R0201


class Answer:
    """Answer"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class AnswerSchema(Schema):
    """Marshmallow answer schema"""
    id = fields.Int()
    datetime = fields.DateTime
    answer = fields.Str(required=True)
    uid = fields.Str(requided=True)

    @post_load
    def make_answer(self, data):
        """Deserializes data into an Answer object"""
        return Answer(**data)
