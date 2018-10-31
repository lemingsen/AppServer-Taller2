"""Base models"""
from pymongo import ReturnDocument
from flask import abort
from bson.objectid import ObjectId
import bson.objectid
from marshmallow import ValidationError
from appserver import mongo


class BaseMapper:
    """Base models class"""
    collection = None
    schema = None

    @classmethod
    def get_by_id(cls, oid):
        """Devuelve un documento con ObjectId oid. Si no existe el documento
        devuelve None"""
        ret = None
        if not bson.objectid.ObjectId.is_valid(oid):
            raise ValidationError("Invalid ObjectId")
        document = mongo.db[cls.collection].find_one({"_id": ObjectId(oid)})
        if document is not None:
            ret = cls.schema.load(document)
        return ret

    @classmethod
    def get_one(cls, filters=None):
        """Devuelve un documento que coincida con los atributos
        pasados en filters. Si no existe un documento que coincida con
        los parámetro de búsqueda devuelve None"""
        ret = None
        document = mongo.db[cls.collection].find_one(filters)
        if document is not None:
            ret = cls.schema.load(document)
        return ret

    @classmethod
    def get_many(cls, filters=None):
        """Devuelve los documentos que coincidan con los parámetros de
        búsqueda pasados en filters. Si no existe ningún documento devuelve
        None"""
        ret = []
        documents = mongo.db[cls.collection].find(filters)
        if documents.count():
            ret = cls.schema.load(documents, many=True)
        return ret

    @classmethod
    def insert(cls, model):
        """Inserta un documento. Devuelve el ObjectId del nuevo documento"""
        data = cls.schema.dump(model)
        result = mongo.db[cls.collection].insert_one(data)
        return result.inserted_id

    @classmethod
    def modify(cls, filters, model):
        """Modifica un documento con el nuevo pasado en object. Si no lo encuentra
        lanza una excepción NotFound"""
        data = cls.schema.dump(model)
        document = mongo.db[cls.collection].find_one_and_replace\
            (filters, data, return_document=ReturnDocument.AFTER)
        if document is None:
            abort(404)
        ret = cls.schema.load(document)
        return ret

    @classmethod
    def find_one_and_update(cls, filters, update):
        """Busca un documento que coincida con los parámetros pasados en filters y actualiza
        los campos pasados en update"""
        ret = None
        document = mongo.db[cls.collection].find_one_and_update\
            (filters, update, return_document=ReturnDocument.AFTER)
        if document is not None:
            ret = cls.schema.load(document)
        return ret

    @classmethod
    def delete_one_by_id(cls, oid):
        """Borra un documento por su ObjectId"""
        ret = False
        if not bson.objectid.ObjectId.is_valid(oid):
            raise ValidationError("Invalid ObjectId")
        result = mongo.db[cls.collection].delete_one({"_id": ObjectId(oid)})
        if result.deleted_count:
            ret = True
        return ret
