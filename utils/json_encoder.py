"""Mongo JSON Encoder"""
from flask.json import JSONEncoder
from bson import ObjectId


class CustomJSONEncoder(JSONEncoder):
    """Mongo JSON Encoder"""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)
