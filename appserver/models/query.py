"""query model"""
from marshmallow import Schema, fields, post_load
# pylint: disable=R0903,R0201


class ProductsQuery:
    """Class for building product queries from the parameters passed in params"""
    def __init__(self, params):
        self.params = params

    def get_query(self):
        """Builds and returns a query from the parameters contained in params dictionary"""
        query = dict()
        if 'text' in self.params:
            query['$or'] = list()
            for text in self.params['text']:
                name = {'name': {'$regex': text, '$options': 'i'}}
                description = {'description': {'$regex': text, '$options': 'i'}}
                query['$or'].append(name)
                query['$or'].append(description)
        if 'units' in self.params:
            units_query = {'units': {'$gte': self.params['units']}}
            query.update(units_query)
        if all(key in self.params for key in ('min_price', 'max_price')):
            min_max_price_query = {
                'price':
                    {'$gte': self.params['min_price'], '$lte': self.params['max_price']}
            }
            query.update(min_max_price_query)
        elif 'max_price' in self.params:
            max_price_query = {'price': {'$lte': self.params['max_price']}}
            query.update(max_price_query)
        elif 'min_price' in self.params:
            min_price_query = {'price': {'$gte': self.params['min_price']}}
            query.update(min_price_query)
        if 'categories' in self.params:
            categories_query = {'categories': {'$in': self.params['categories']}}
            query.update(categories_query)
        if 'payment_methods' in self.params:
            payment_methods_query = {'payment_methods': {'$in': self.params['payment_methods']}}
            query.update(payment_methods_query)
        return query


class ProductsQuerySchema(Schema):
    """ProductsQuery Schema"""
    text = fields.List(fields.Str())
    units = fields.List(fields.Int())
    min_price = fields.List(fields.Float())
    max_price = fields.List(fields.Float())
    x = fields.List(fields.Float())
    y = fields.List(fields.Float())
    categories = fields.List(fields.Str())
    payment_methods = fields.List(fields.Str())

    @post_load
    def make_products_query(self, data):
        """Returns a ProductsQuery object with the parameters passed in data dictionary"""
        keys = ['text', 'units', 'min_price', 'max_price',
                'x', 'y', 'categories', 'payment_methods']
        single_value_keys = ['units', 'min_price', 'max_price', 'x', 'y']
        params = dict()
        for key in keys:
            if key in data:
                if key in single_value_keys:
                    params[key] = data[key][0]
                else:
                    params[key] = data[key]
        return ProductsQuery(params)
