from flask import Blueprint
from flask_restplus import Api
from .hello import api as hello

blueprint = Blueprint('api', __name__)
api = Api(blueprint, title='Shared Server API',version='1.0',description='A description')
api.add_namespace(hello)


