"""controllers init"""
from flask import Blueprint
# pylint: disable=C0103,C0413

api_bp = Blueprint('controllers', __name__)
from appserver.controllers import root_controllers, user_controllers,\
    product_controllers, order_controllers, handlers
