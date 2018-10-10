"""Base model"""
from pymongo import ReturnDocument
from flask import abort
from bson.objectid import ObjectId
from app import db



class Model:
    """Base model class"""
    collection_name = None
    db_name = 'comprame'

    def __init__(self, data):
        """Sets attributes from data dictionary"""
        self._id = None
        for key in data:
            setattr(self, key, data[key])

    @classmethod
    def get_one_or_404(cls, query=None):
        """Devuelve un documento que coincida con los atributos
         pasados en query. Si no hay ningún documento que coincida
         se lanza una excepción NotFound"""
        document = db[cls.collection_name].find_one(query)
        if document is None:
            abort(404)
        return document

    @classmethod
    def get_by_id_or_404(cls, oid):
        """Devuelve un documento con ObjectId oid. Si no existe el documento
        se lanza una excepción NotFound"""
        document = db[cls.collection_name].find_one({"_id": ObjectId(oid)})
        if document is None:
            abort(404)
        return document

    @classmethod
    def get_one(cls, query=None):
        """Devuelve un documento que coincida con los atributos
        pasados en query. Si no existe un documento que coincida con
        los parámetro de búsqueda devuelve None"""
        document = db[cls.collection_name].find_one(query)
        return document

    @classmethod
    def get_many_or_404(cls, query):
        """Devuelve los documentos que coincidan con los parámetros de
        búsqueda pasados en filter. Si no existe ningún documento se lanza
        una excepción NotFound"""
        documents = db[cls.collection_name].find(query)
        if documents is None:
            abort(404)
        return documents

    @classmethod
    def insert(cls, data):
        """Inserta un documento. Devuelve el ObjectId del nuevo documento"""
        result = db[cls.collection_name].insert_one(data)
        return result.inserted_id

    @classmethod
    def modify(cls, query, data):
        """Modifica un documento con el nuevo pasado en data. Si no lo encuentra
        lanza una excepción NotFound"""
        document = db[cls.collection_name].find_one_and_replace\
            (query, data, return_document=ReturnDocument.AFTER)
        if document is None:
            abort(404)
        return document
