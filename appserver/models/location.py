"""Location models"""
from math import sin, cos, sqrt, atan2, radians
from marshmallow import Schema, fields, post_load
# pylint: disable=R0903,R0201, C0103


class Location:
    """Location"""
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    def distance_to(self, other_location):
        """Returns distance in kilometers between two points"""
        earth_radius = 6373.0
        long2 = radians(other_location.longitude)
        lat2 = radians(other_location.latitude)
        long1 = radians(self.longitude)
        lat1 = radians(self.latitude)
        delta_longitude = long2 - long1
        delta_latitude = lat2 - lat1
        a = (sin(delta_latitude / 2)) ** 2 + cos(lat1) * \
            cos(lat2) * (sin(delta_longitude / 2)) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = earth_radius * c
        return distance


class LocationSchema(Schema):
    """Location marshmallow schema"""
    longitude = fields.Float(required=True)
    latitude = fields.Float(required=True)

    @post_load
    def make_location(self, data):
        """Deserializes data into a Location object"""
        return Location(data['longitude'], data['latitude'])
