"""Hello World"""
from flask_restplus import Namespace, Resource

api = Namespace('hello', description='Hello World namespace')


@api.route('/')
class HelloWorld(Resource):
    """hello route"""
    def get(self):
        """hello GET"""
        return {'hello': 'world'}
