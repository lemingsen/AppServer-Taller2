"""api init"""
from flask_restplus import Api
from .root import ns as root
from .user import ns as user
from .purchases import ns as purchases


api = Api(title='Application Server API',
          version='1.0', description='Comprame Application Server API')
api.namespaces.clear()
api.add_namespace(root)
api.add_namespace(user)
api.add_namespace(purchases)
