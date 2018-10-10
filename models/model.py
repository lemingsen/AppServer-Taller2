from app import db
from pymongo import ReturnDocument
from flask import abort


class Model:
    collection_name = None
    db_name = 'comprame'

    def __init__(self, data):
        self._id = None
        for key in data:
            setattr(self, key, data[key])

    @classmethod
    def get_one(cls, query):
        document = db[cls.collection_name].find_one(query)
        if document is None:
            abort(404)
        return document

    @classmethod
    def get_many(cls, query):
        documents = db[cls.collection_name].find(query)
        if documents is None:
            abort(404)
        return documents

    @classmethod
    def insert(cls, data):
        result = db[cls.collection_name].insert_one(data)
        return result.inserted_id

    @classmethod
    def modify(cls, filter, data):
        document = db[cls.collection_name].find_one_and_replace\
            (filter, data, return_document=ReturnDocument.AFTER)
        if document is None:
            abort(404)
        return document


