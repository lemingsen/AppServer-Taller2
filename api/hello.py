from flask_restplus import Namespace, Resource

api = Namespace('hello', description='Hello World namespace')

@api.route('/')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}