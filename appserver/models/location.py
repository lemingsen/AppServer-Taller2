"""Location models"""
from math import sin, cos, sqrt, atan2, radians
from marshmallow import Schema, fields, post_load, validate
# pylint: disable=R0903,R0201, C0103


class Location:
    """Location"""
    def __init__(self, coordinates):
        self.coordinates = [coordinates[0], coordinates[1]]

    def distance_to(self, other_location):
        """Returns distance in kilometers between two points"""
        earth_radius = 6373.0
        long2 = radians(other_location.coordinates[0])
        lat2 = radians(other_location.coordinates[1])
        long1 = radians(self.coordinates[0])
        lat1 = radians(self.coordinates[1])
        delta_longitude = long2 - long1
        delta_latitude = lat2 - lat1
        a = (sin(delta_latitude / 2)) ** 2 + cos(lat1) * \
            cos(lat2) * (sin(delta_longitude / 2)) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = earth_radius * c
        return distance


class LocationSchema(Schema):
    """Location marshmallow schema"""
    coordinates = fields.List(fields.Float(), validate=validate.Length(
        min=2, max=2, error="Wrong coordinate"), required=True)

    @post_load
    def make_location(self, data):
        """Deserializes data into a Location object"""
        return Location(data['coordinates'])


class LocationModifySchema(Schema):
    """LocationModifySchema"""
    coordinates = fields.List(fields.Float(), required=True)
