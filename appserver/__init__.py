"""Main"""
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from appserver.utils.mongo import MongoJSONEncoder


mongo = PyMongo()
jwt = JWTManager()


def create_app(config):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['MONGO_URI'] = os.environ['MONGO_URI']
    app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
    mongo.init_app(app)
    app.json_encoder = MongoJSONEncoder
    jwt.init_app(app)

    from appserver.controllers import api
    app.register_blueprint(api)

    return app
