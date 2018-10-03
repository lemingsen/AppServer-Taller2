"""Product"""
import requests
from api import api


@api.route('/tracking/<int:track_id>', methods=['GET'])
def track(track_id):
    """Servicio de tracking: permite conocer el estado de una
     compra a través del código de tracking"""
    req = requests.get('https://shared-server-tallerii.herokuapp.com/envios/' + str(track_id))
    return req.json()
