"""MongoDB utilities"""
from flask.json import JSONEncoder
import bson
from marshmallow import fields, ValidationError, missing


class MongoJSONEncoder(JSONEncoder):
    """Encodes mongodb ObjectId"""
    def default(self, o):
        if isinstance(o, bson.ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)


class ObjectId(fields.Field):
    """Extends marshmallow Field to add mongodb ObjectId as a field"""
    def _deserialize(self, value, attr, data):
        try:
            return bson.ObjectId(value)
        except:
            raise ValidationError('invalid ObjectId `%s`' % value)

    def _serialize(self, value, attr, obj):
        if value is None:
            return missing
        return str(value)
