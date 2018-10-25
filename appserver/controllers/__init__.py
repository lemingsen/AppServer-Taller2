"""controllers init"""
from flask import Blueprint

api = Blueprint('controllers', __name__)
from appserver.controllers import root_controller, users_controller, products_controller, handlers
