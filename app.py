"""Main"""
from flask import Flask
from api import api
from config import DevelopmentConfig
from pymongo import MongoClient
import firebase_admin
from firebase_admin import credentials
from flask_jwt_extended import JWTManager
from flask import abort


cred = credentials.Certificate('comprameli-49a1b-firebase-adminsdk-2tc0n-f9160f71dc.json')
firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
client = MongoClient(app.config["DATABASE_URI"])
api.init_app(app)
app.config['JWT_SECRET_KEY'] = 'esta es la clave secreta'
jwt = JWTManager(app)


if __name__ == '__main__':
    app.run(debug=True)




