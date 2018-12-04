"""Shared Server Services"""
import os
import json
from datetime import datetime
from functools import wraps
from werkzeug.exceptions import BadGateway
import requests
from marshmallow import Schema, fields, post_load
from appserver.models.order import TrackingInfoSchema
from appserver.services.exceptions import ExpiredTokenError
from appserver.models.payment_method import PaymentMethodSchema
# pylint: disable=R0903,R0201


class SharedServerCredentials:
    """SharedServerCredentials"""
    def __init__(self, server_id, token):
        self.server_id = server_id
        self.token = token


class SharedServerCredentialSchema(Schema):
    """SharedServerCredentials schema"""
    server_id = fields.Int(required=True)
    token = fields.Str(required=True)

    @post_load
    def make_server_credentials(self, data):
        """Returns a SharedServerCredential object from data dict"""
        return SharedServerCredentials(**data)


def refresh_token(func):
    """Refresh token decorator"""
    @wraps(func)
    def wrapper_refresh_token(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ExpiredTokenError:
            SharedServer.refresh_access_token()
            return func(*args, **kwargs)
    return wrapper_refresh_token


class SharedServer:
    """Wraps all shared server operations"""
    server_credentials = None
    auth_token = None
    shared_server_uri = os.environ['SHARED_SERVER_URI']
    schema = SharedServerCredentialSchema()

    def __init__(self):
        self.filename = os.environ['SHARED_SERVER_FILE']
        try:
            server_file = open(self.filename, 'r')
            SharedServer.server_credentials = self.schema.load(json.load(server_file))
        except FileNotFoundError:
            pass

    def _register_app_server(self):
        """Registers the server in the shared server"""
        url = os.environ['SHARED_SERVER_URI'] + '/servers'
        payload = {
            'createdBy': 'App Server',
            'name': 'App Server'
        }
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            response_payload = response.json()
            token = response_payload['server']['token']['token']
            server_id = response_payload['server']['server']['id']
            server_file = open(self.filename, 'w')
            server_credentials = {'server_id': server_id, 'token': token}
            json.dump(server_credentials, server_file)
            SharedServer.server_credentials = self.schema.load(server_credentials)

    @classmethod
    def refresh_access_token(cls):
        """Refreshes access token for shared server"""
        url = os.environ['SHARED_SERVER_URI'] + '/servers/' + str(cls.server_credentials.server_id)
        header = {'Authorization': 'Bearer ' + cls.server_credentials.token}
        response = requests.post(url, headers=header)
        if response.status_code == 201:
            response_payload = response.json()
            SharedServer.auth_token = response_payload['server']['token']['token']

    def init(self):
        """Registers server in shared server and gets a new access token"""
        if self.server_credentials is None:
            self._register_app_server()
        SharedServer.refresh_access_token()

    @refresh_token
    def new_tracking(self):
        """Returns a new tracking number for an order from shared server"""
        product_tracking = None
        tracking_code_schema = TrackingInfoSchema()
        url = os.environ['SHARED_SERVER_URI'] + '/tracking'
        header = {'Authorization': 'Bearer ' + self.auth_token}
        response = requests.post(url, headers=header)
        if response.status_code == 201:
            product_tracking = tracking_code_schema.load(response.json())
        if response.status_code == 401:
            raise ExpiredTokenError()
        return product_tracking.id

    @refresh_token
    def create_payment(self, order):
        """Sends a new payment order to shared server"""
        url = os.environ['SHARED_SERVER_URI'] + '/payments'
        header = {'Authorization': 'Bearer ' + self.auth_token}
        payload = {
            "transaction_id": order.tracking_number,
            "currency": "Pesos",
            "value": order.total,
            "paymentMethod": {
                "expiration_date": order.payment_info.expiration_date,
                "payment_method": order.payment_info.payment_method,
                "card_number": order.payment_info.card_number,
                "security_code": order.payment_info.security_code,
                "cardholder_name": order.payment_info.cardholder_name
            }
        }
        response = requests.post(url, headers=header, json=payload)
        if response.status_code == 401:
            raise ExpiredTokenError()
        if response.status_code != 201:
            raise BadGateway()

    @refresh_token
    def update_tracking_status(self, order):
        """Returns the shipping order status from shared server"""
        url = os.environ['SHARED_SERVER_URI'] + '/tracking/' + str(order.tracking_number)
        header = {'Authorization': 'Bearer ' + self.auth_token}
        response = requests.get(url, headers=header)
        tracking_status = {
            'PENDIENTE': 'PENDIENTE DE ENVIO',
            'EN TRANSITO': 'ENVIO EN PROGRESO',
            'CANCELADO': 'ENVIO CANCELADO',
            'ENTREGADO': 'ENVIO REALIZADO'
        }
        if response.status_code == 401:
            raise ExpiredTokenError()
        if response.status_code == 200:
            tracking_list = response.json()
            if tracking_list:
                tracking_last_update = tracking_list[-1]
            status = tracking_last_update['status']
            order.last_status_update = datetime.now()
            # order.last_status_update = tracking_last_update['updateat']
            order.status = tracking_status[status]
        else:
            raise BadGateway()

    @refresh_token
    def update_payment_status(self, order):
        """Updates the order payment status from shared server"""
        url = os.environ['SHARED_SERVER_URI'] + '/payments/id/' + str(order.tracking_number)
        header = {'Authorization': 'Bearer ' + self.auth_token}
        response = requests.get(url, headers=header)
        payment_status = {
            'PENDIENTE': 'PAGO PENDIENTE DE PROCESO',
            'CONFIRMADO': 'PAGO ACEPTADO',
            'CANCELADO': 'PAGO RECHAZADO'
        }
        if response.status_code == 401:
            raise ExpiredTokenError()
        if response.status_code == 200:
            payment_list = response.json()
            if payment_list:
                payment_last_update = payment_list[-1]
            status = payment_last_update['status']
            order.last_status_update = datetime.now()
            # order.last_status_update = payment_last_update['updateat']
            order.status = payment_status[status]
        else:
            raise BadGateway()

    @refresh_token
    def get_delivery_estimate(self, order, buyer):
        """Returns a shipping cost estimation for an order from shared server"""
        url = os.environ['SHARED_SERVER_URI'] + '/deliveries/estimate'
        header = {'Authorization': 'Bearer ' + self.auth_token}
        payload = {
            "ammount": order.units,
            "distance": order.product_location.distance_to(order.buyer_location),
            "user": {
                "email": buyer.email,
                "points": buyer.points,
                "deliveries": buyer.purchases
            }
        }
        response = requests.post(url, headers=header, json=payload)
        if response.status_code == 401:
            raise ExpiredTokenError()
        if response.status_code == 201:
            delivery_estimate = response.json()
            cost = delivery_estimate['cost']
        else:
            raise BadGateway()
        return cost

    @refresh_token
    def get_payment_methods(self):
        """Returns available payment methods from shared server"""
        url = os.environ['SHARED_SERVER_URI'] + '/payments/methods'
        header = {'Authorization': 'Bearer ' + self.auth_token}
        response = requests.get(url, headers=header)
        if response.status_code == 401:
            raise ExpiredTokenError()
        if response.status_code == 200:
            payment_methods = []
            payment_methods_dict = response.json()
            for payment_method in payment_methods_dict:
                payment_methods.append(PaymentMethodSchema().load(payment_method))
        else:
            raise BadGateway()
        return payment_methods
