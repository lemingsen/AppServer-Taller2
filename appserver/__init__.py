"""Main"""
from flask import Flask
from flask_jwt_extended import JWTManager
import firebase_admin as firebase
from flask_pymongo import PyMongo
import os
from appserver.utils.mongo_encoder import MongoJSONEncoder
from appserver.service.product import Product, Location, LocationSchema, ProductSchema


mongo = PyMongo()
jwt = JWTManager()


def create_app(config):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['MONGO_URI'] = os.environ['MONGO_URI']
    app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
    mongo.init_app(app)
    try:
        firebase.get_app()
    except ValueError:
        cred = firebase.credentials.Certificate(os.environ['FIREBASE_CONFIG'])
        firebase.initialize_app(cred)
    app.json_encoder = MongoJSONEncoder
    jwt.init_app(app)

    from appserver.controllers import api
    app.register_blueprint(api)

    return app
