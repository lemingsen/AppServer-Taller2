"""Answer models"""
from marshmallow import Schema, fields, post_load, validate
# pylint: disable=R0903,R0201


class Answer:
    """Answer"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class AnswerSchema(Schema):
    """Marshmallow answer schema"""
    answer_id = fields.Str()
    datetime = fields.Str()
    answer = fields.Str(required=True, validate=validate.Length(
        min=1, error="Answer cannot be empty."))
    uid = fields.Str()

    @post_load
    def make_answer(self, data):
        """Deserializes data into an Answer object"""
        return Answer(**data)
