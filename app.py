"""Main"""
from flask import Flask
from api import api
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
api.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
