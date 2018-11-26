"""Main"""
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flasgger import Swagger
from appserver.utils.mongo import MongoJSONEncoder
from appserver.config import DevelopmentConfig
# pylint: disable=C0103

mongo = PyMongo()
jwt = JWTManager()
swagger = Swagger(template_file=os.environ['SWAGGER_FILE'])


def create_app(config=DevelopmentConfig):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['MONGO_URI'] = os.environ['MONGO_URI']
    app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
    mongo.init_app(app)
    app.json_encoder = MongoJSONEncoder
    jwt.init_app(app)
    app.config['SWAGGER'] = {
        'title': 'Comprame App Server API',
        'uiversion': 2
    }
    swagger.init_app(app)

    from appserver.controllers import api_bp
    app.register_blueprint(api_bp)

    return app
