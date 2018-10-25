"""Product Services"""
from datetime import datetime
from appserver.model.product import ProductSchema
from appserver.data.product_mapper import ProductMapper
from appserver.service.exceptions import NotFoundError


class ProductsService:
    """Product Services"""
    schema = ProductSchema()

    @classmethod
    def add_product(cls, product_json):
        """Add product service:"""
        product = cls.schema.load(product_json)
        product.published = str(datetime.now())
        return ProductMapper.insert(product)

    @classmethod
    def get_product_by_id(cls, product_id):
        """Get product by id service:"""
        product = ProductMapper.get_by_id(product_id)
        if product is None:
            raise NotFoundError("Product not found.")
        return cls.schema.dump(product)

    @classmethod
    def get_products(cls, filters=None):
        """Get products service: returns all the
         products that match with filters parameters"""
        ret = []
        products = ProductMapper.get_many(filters)
        if not products:
            raise NotFoundError("No product matches the query.")
        for product in products:
            ret.append(cls.schema.dump(product))
        return ret

    @classmethod
    def add_question(cls, product_id):
        """Add question service: adds a question to the product
        with id product_id"""
        pass

    @classmethod
    def add_answer(cls, product_id, question_id):
        """Add answer service: adds an answer to question_id question in
         product_id product"""
        pass

    @classmethod
    def buy(cls, seller_id, buyer_id, quantity):
        """Buy product service:"""
        pass
