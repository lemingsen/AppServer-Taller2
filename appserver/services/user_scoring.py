"""User Scoring"""
from appserver.data.user_mapper import UserMapper
from appserver.data.product_mapper import ProductMapper


class UserScoring:
    """Manages user points"""
    def __init__(self, uid):
        self.uid = uid
        self.points_new_order_buyer = 2
        self.points_new_order_seller = 2
        self.points_new_product = 1
        self.points_positive_rating = 3
        self.points_neutral_rating = 1
        self.points_negative_rating = -2

    def new_purchase(self):
        """Updates points for user after a new purchase"""
        self._update_points(self.points_new_order_buyer)

    def new_sale(self):
        """Updates points for user after a new sale"""
        self._update_points(self.points_new_order_seller)

    def new_product(self):
        """Updates points for user after publishing a new product"""
        self._update_points(self.points_new_product)

    def new_rating(self, rating):
        """Updates points for user after receiving a new rating"""
        if rating == 'POSITIVE':
            points = self.points_positive_rating
        if rating == 'NEGATIVE':
            points = self.points_negative_rating
        if rating == 'NEUTRAL':
            points = self.points_neutral_rating
        self._update_points(points)

    def _update_points(self, points):
        print(self.uid)
        print(points)
        user = UserMapper.add_points(self.uid, points)
        print(user.points)
        ProductMapper.update_points(self.uid, user.points)
