"""Hello World"""
from flask_restplus import Namespace, Resource

ns = Namespace('user', description='/user')


@ns.route('/auth')
class Login(Resource):
    """Servicio de autenticación"""
    def post(self):
        """Permite a los usuarios poder ingresar al sistema, obteniendo
             un token que deberá ser utilizado por los demás servicios."""
        pass


@ns.route('/register')
class Register(Resource):
    """Servicio de registro"""
    def post(self):
        """Permite a los usuarios darse de alta en el sistema."""
        pass


@ns.route('/profile')
class Profile(Resource):
    """Servicio de perfil de usuario"""
    def get(self):
        """Permite consultar el perfil de un usuario"""
        pass

    def put(self):
        """Permite a un usuario actualizar su perfil"""
        pass
