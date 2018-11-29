"""query model"""
from marshmallow import Schema, fields, post_load, validates_schema, ValidationError, validates
# pylint: disable=R0903,R0201


class ProductsQueryFiltersSchema(Schema):
    """Products query filters Schema"""
    text = fields.List(fields.Str())
    units = fields.Int()
    min_price = fields.Float()
    max_price = fields.Float()
    categories = fields.List(fields.Str())
    payment_methods = fields.List(fields.Str())
    seller = fields.Str()
    longitude = fields.Float()
    latitude = fields.Float()
    min_distance = fields.Float()
    max_distance = fields.Float()

    @post_load
    def coordinates_to_list(self, data):
        """Replaces the longitude and latitude dictionary
         entries with a coordinates entry being a list of both values"""
        if data.get('longitude'):
            longitude = data.pop('longitude')
            latitude = data.pop('latitude')
            data['coordinates'] = [longitude, latitude]
        return data

    def check_valid_coordinates(self, data):
        """Checks that both longitude and
        latitude filters are sent or none of the two"""
        missing_latitude = data.get('longitude') and not data.get('latitude')
        missing_longitude = not data.get('longitude') and data.get('latitude')
        if missing_latitude or missing_longitude:
            raise ValidationError("latitude and longitude parameters"
                                  " are required to establish a coordinate.")

    def check_valid_distance(self, data):
        """Checks that if distance filters are sent,
         then longitude and latitude must exist"""
        present_distance_field = data.get('min_distance') or data.get('max_distance')
        missing_coordinates = not data.get('longitude') and not data.get('latitude')
        if present_distance_field and missing_coordinates:
            raise ValidationError("latitude and longitude parameters are required"
                                  " with min_distance or max_distance parameters")

    @validates_schema
    def validate_location_data(self, data):
        """Validates location filters"""
        self.check_valid_coordinates(data)
        self.check_valid_distance(data)

    @validates('longitude')
    def validate_longitude(self, value):
        """Longitude filter validation"""
        if value < -180 or value > 180:
            raise ValidationError("longitude must be between -180 and 180")

    @validates('latitude')
    def validate_latitude(self, value):
        """Latitude filter validation"""
        if value < -90 or value > 90:
            raise ValidationError("latitude must be between -90 and 90")

    @validates('min_price')
    def validate_min_price(self, value):
        """Minimum price filter validation"""
        if value < 0:
            raise ValidationError("min_price must be greater or equal to 0.")

    @validates('max_price')
    def validate_max_price(self, value):
        """Maximum price filter validation"""
        if value < 0:
            raise ValidationError("max_price must be greater or equal to 0.")

    @validates('min_distance')
    def validate_min_distance(self, value):
        """Minimum price filter validation"""
        if value < 0:
            raise ValidationError("min_distance must be greater or equal to 0.")

    @validates('max_distance')
    def validate_max_distance(self, value):
        """Maximum distance filter validation"""
        if value < 0:
            raise ValidationError("max_distance must be greater or equal to 0.")

    @validates('units')
    def validate_units(self, value):
        """Units filter validation"""
        if value < 1:
            raise ValidationError("units must be greater than 0.")
