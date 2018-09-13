"""Root"""
from flask_restplus import Namespace, Resource

ns = Namespace('root', path='/', description='/')


@ns.route('/ping')
class Ping(Resource):
    """Servicio de estado"""
    def get(self):
        """Brinda una respuesta rápida que permita ser consultada
        para conocer si el servidor se encuentra activo"""
        return {'ping': 1}


@ns.route('/stats')
class Stats(Resource):
    """Servicio de consulta de datos de uso"""
    def get(self):
        """Brinda datos acerca del uso del application server."""
        return {'hello': 'world'}


@ns.route('/hello')
class HelloWorld(Resource):
    """Hello World"""
    def get(self):
        """Devuelve Hello World"""
        return {'hello': 'world'}
