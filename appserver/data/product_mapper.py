"""product models"""
from appserver.models.product import ProductSchema
from appserver.data.base_mapper import BaseMapper
from appserver.app import mongo
# pylint: disable=R0903


class ProductMapper(BaseMapper):
    """product models"""
    collection = 'products'
    schema = ProductSchema()

    @classmethod
    def query(cls, filters):
        """Queries the product collection with the filters sent"""
        query_builder = ProductsQueryBuilder(filters)
        query = query_builder.get_pipeline()
        documents = mongo.db[cls.collection].aggregate(query)
        return documents


class ProductsQueryBuilder:
    """Class for building product queries from the filters passed"""
    def __init__(self, filters):
        self.location_pipe = dict()
        self.query_pipe = dict()
        self.filters = filters

    def _coordinates_query(self, param):
        query = {
            'near': {'type': 'Point', 'coordinates': param},
            'spherical': 'true',
            'distanceField': 'distance'
        }
        self.location_pipe.update(query)

    def _min_distance_query(self, param):
        query = {'minDistance': param}
        self.location_pipe.update(query)

    def _max_distance_query(self, param):
        query = {'maxDistance': param}
        self.location_pipe.update(query)

    def _text_query(self, param):
        self.query_pipe['$or'] = list()
        for text in param:
            name = {'name': {'$regex': text, '$options': 'i'}}
            description = {'description': {'$regex': text, '$options': 'i'}}
            self.query_pipe['$or'].append(name)
            self.query_pipe['$or'].append(description)

    def _units_query(self, param):
        query = {'units': {'$gte': param}}
        self.query_pipe.update(query)

    def _min_price_query(self, param):
        query = {'price': {'$gte': param}}
        self.query_pipe.update(query)

    def _max_price_query(self, param):
        query = {'price': {'$lte': param}}
        self.query_pipe.update(query)

    def _categories_query(self, param):
        query = {'categories': {'$in': param}}
        self.query_pipe.update(query)

    def _payment_methods_query(self, param):
        query = {'payment_methods.name': {'$in': param}}
        self.query_pipe.update(query)

    def _seller_query(self, param):
        query = {'seller': param}
        self.query_pipe.update(query)

    def _dispatch(self, key):
        dispatcher = {
            'text': self._text_query,
            'units': self._units_query,
            'min_price': self._min_price_query,
            'max_price': self._max_price_query,
            'categories': self._categories_query,
            'payment_methods': self._payment_methods_query,
            'seller': self._seller_query,
            'coordinates': self._coordinates_query,
            'min_distance': self._min_distance_query,
            'max_distance': self._max_distance_query
        }

        dispatcher[key](self.filters[key])

    def get_pipeline(self):
        """Builds and returns a query from
        the parameters contained in params dictionary"""
        pipeline = list()
        for key in self.filters:
            self._dispatch(key)

        if self.location_pipe:
            geonear_aggregate = dict()
            geonear_aggregate['$geoNear'] = self.location_pipe
            pipeline.append(geonear_aggregate)

        if self.query_pipe:
            match_aggregate = dict()
            match_aggregate['$match'] = self.query_pipe
            pipeline.append(match_aggregate)
        return pipeline
