"""Main"""
from flask import Flask
from config import DevelopmentConfig
from pymongo import MongoClient
import firebase_admin
from firebase_admin import credentials
from flask_jwt_extended import JWTManager



cred = credentials.Certificate('comprameli-49a1b-firebase-adminsdk-2tc0n-f9160f71dc.json')
firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
client = MongoClient(app.config["DATABASE_URI"])
db = client[app.config["DATABASE_NAME"]]
app.config['JWT_SECRET_KEY'] = 'esta es la clave secreta'
jwt = JWTManager(app)

from api import api
app.register_blueprint(api)


if __name__ == '__main__':
    app.run(debug=True)




