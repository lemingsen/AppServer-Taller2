"""Product"""
from flask_restplus import Namespace, Resource
import requests

ns = Namespace('purchases', description='/purchases')


@ns.route('/tracking/<int:track_id>')
class Tracking(Resource):
    """Servicio de tracking"""
    def get(self, track_id):
        """Permite conocer el estado de una
         compra a través del código de tracking"""
        req = requests.get('https://shared-server-tallerii.herokuapp.com/envios/' + str(track_id))
        return req.json()
