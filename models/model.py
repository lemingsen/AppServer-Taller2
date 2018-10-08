from app import db
from bson.objectid import ObjectId


class Model:
    collection_name = None
    db_name = 'comprame'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_one(cls, **kwargs):
        document = db[cls.collection_name].find_one(**kwargs)
        return document

    @classmethod
    def get_one(cls, id):
        document = db[cls.collection_name].find_one(({'_id': ObjectId(id)}))
        return document

    @classmethod
    def get_many(cls, **kwargs):
        documents = db[cls.collection_name].find(**kwargs)
        return documents

    @classmethod
    def insert(cls, data):
        result = db[cls.collection_name].insert_one(data)
        return result.inserted_id

    def remove(self):
        pass

    def save(self):
        pass


