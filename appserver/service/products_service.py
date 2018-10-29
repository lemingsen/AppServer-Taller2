"""Product Services"""
from datetime import datetime
from appserver.model.product import ProductSchema
from appserver.data.product_mapper import ProductMapper
from appserver.service.exceptions import NotFoundError, ForbiddenError


class ProductsService:
    """Product Services"""
    schema = ProductSchema()

    @classmethod
    def add_product(cls, product_json, uid):
        """Add product service:"""
        product_json['seller'] = uid
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
    def delete_product(cls, uid, product_id):
        """Delete product service: deletes product product_id from user uid."""
        if cls._product_exists_and_belongs_to_user(uid, product_id):
            if not ProductMapper.delete_one_by_id(product_id):
                raise NotFoundError("Product not found.")
        return True

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

    @classmethod
    def _product_exists_and_belongs_to_user(cls, uid, product_id):
        """Checks if product exists and belongs to user."""
        product = ProductMapper.get_by_id(product_id)
        if product is None:
            raise NotFoundError("Product does not exist.")
        if product.seller != uid:
            raise ForbiddenError("User can only delete his own products")
        return True
