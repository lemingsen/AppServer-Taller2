import pytest
import appserver
from appserver.config import TestingConfig
from appserver.models.product import ProductSchema
from appserver.models.payment_method import PaymentMethodSchema
from appserver.models.order import OrderSchema
from appserver.models.user import UserSchema


class Data:
    def __init__(self):
        self.valid_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MzgwNzUyODUsIm5iZiI6MTUzODA3NTI4NSwianRpI' \
                 'joiMzIxNmEwN2MtODM3ZS00ZDFjLWIxOTEtNTg0YjY2NGVkMTgzIiwiaWRlbnRpdHkiOiJZbWpnWk0wNmpWV3JiR25PdVVm' \
                 'VEl0TU1aeDIyIiwiZnJlc2giOnRydWUsInR5cGUiOiJhY2Nlc3MifQ.HKYLK2RwLfEwigWA_OfUItLATT7XgVxnfatmjp4feWY'
        self.invalid_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MzgwNzUyODUsIm5iZiI6MTUzODA3NTI4NSwianRpI' \
                 'joiMzIxNmEwN2MtODM3ZSxLWIxOTEtNTg0YjY2NGVkMTgzIiwiaWRlbnRpdHkiOiJZbWpnWk0wNmpWV3JiR25PdVVm' \
                 'VEl0TU1aeDIyIiwiZnJlc2giOnRydWUsInR5cGUiOiJhY2Nlc3MifQ.HKYLK2RwLfEwigWA_OfUItLATT7XgVxnfatmjp4feWY'

    def valid_token_header(self):
        return {'Authorization': 'Bearer ' + self.valid_token}

    def invalid_token_header(self):
        return {'Authorization': 'Bearer ' + self.invalid_token}

    def empty_json(self):
        return {}

    def not_json(self):
        return "hola"


class OrderData(Data):
    def __init__(self):
        Data.__init__(self)

        self.estimate_shipping_input_data = {
            "product_id": "5bd7b28bc9133f00087dd8e8",
            "units": 1
        }

        self.positive_rating = {
            "rate": "POSITIVE"
        }

        self.neutral_rating = {
            "rate": "NEUTRAL"
        }

        self.negative_rating = {
            "rate": "NEGATIVE"
        }

        self.invalid_rating = {
            "rate": "MUY BUENO"
        }

        self.valid_input_order = {
            "product_id": "5bd7b28bc9133f00087dd8e8",
            "units": 3,
            "payment_info": {
                "payment_method": "visa",
                "cardholder_name": "Pepe Grillo",
                "card_number": "1234-1234-1234-1234",
                "expiration_date": "11/22",
                "security_code": "123"
            },
            "has_to_be_shipped": False
        }

        self.invalid_input_order = {
            "productid": "5bd7b28bc9133f00087dd8e8",
            "units": 3,
            "payment_info": {
                "payment_method": "visa",
                "cardholder_name": "Pepe Grillo",
                "card_number": "1234-1234-1234-1234",
                "expiration_date": "11/22",
                "security_code": "123"
            },
            "has_to_be_shipped": False
        }

        self.negative_units_input_order = {
            "product_id": "5bd7b28bc9133f00087dd8e8",
            "units": -3,
            "payment_info": {
                "payment_method": "visa",
                "cardholder_name": "Pepe Grillo",
                "card_number": "1234-1234-1234-1234",
                "expiration_date": "11/22",
                "security_code": "123"
            },
            "has_to_be_shipped": False
        }

        self.input_order_with_9_units = {
            "payment_info": {
                "payment_method": "Mastercard",
                "security_code": "125",
                "card_number": "1234-1322-1223-1223",
                "cardholder_name": "Pepe Gutierrez",
                "expiration_date": "01/22"
            },
            "units": 9,
            "product_id": "5bd7b28bc9133f00087dd8e8",
            "has_to_be_shipped": False
        }

        self.order_with_delivery_and_not_shipped = {
            "_id": "5c107700e3c00c56a904cb9b",
            "buyer": "YmjgZM06jVWrbGnOuUfTItMMZx22",
            "buyer_info": {
                "email": "lucas@gmail.com",
                "username": "Lucas"
            },
            "buyer_location": {
                "latitude": -34.6,
                "longitude": -58.5
            },
            "has_to_be_shipped": True,
            "payment_info": {
                "card_number": "1234-1322-1223-1223",
                "cardholder_name": "Pepe Gutierrez",
                "expiration_date": "01/22",
                "payment_method": "Mastercard",
                "security_code": "123"
            },
            "product_id": "5bd7b28bc9133f00087dd8e8",
            "product_location": {
                "latitude": -34.558499,
                "longitude": -58.466767
            },
            "product_name": "Placa de video ATI 5750",
            "products_total": 450000,
            "seller": "YmjgZM06yVWrbGnuUfTIo9MZx28",
            "seller_info": {
                "email": "lucas@gmail.com",
                "username": "Lucas Hemmingsen"
            },
            "shipping_cost": 1000,
            "status": "PAGO ACEPTADO",
            "total": 451000,
            "tracking_number": 148,
            "units": 15
        }

        self.order_with_delivery_and_shipped = {
            "_id": "5c107700e3c00c56a904cb9b",
            "buyer": "YmjgZM06jVWrbGnOuUfTItMMZx22",
            "buyer_info": {
                "email": "lucas@gmail.com",
                "username": "Lucas"
            },
            "buyer_location": {
                "latitude": -34.6,
                "longitude": -58.5
            },
            "has_to_be_shipped": True,
            "payment_info": {
                "card_number": "1234-1322-1223-1223",
                "cardholder_name": "Pepe Gutierrez",
                "expiration_date": "01/22",
                "payment_method": "Mastercard",
                "security_code": "123"
            },
            "product_id": "5bd7b28bc9133f00087dd8e8",
            "product_location": {
                "latitude": -34.558499,
                "longitude": -58.466767
            },
            "product_name": "Placa de video ATI 5750",
            "products_total": 450000,
            "seller": "YmjgZM06yVWrbGnuUfTIo9MZx28",
            "seller_info": {
                "email": "lucas@gmail.com",
                "username": "Lucas Hemmingsen"
            },
            "shipping_cost": 1000,
            "status": "ENVIO REALIZADO",
            "total": 451000,
            "tracking_number": 148,
            "units": 15
        }

        self.order_without_delivery_and_not_payed = {
            "_id": "5c107700e3c00c56a904cb9b",
            "buyer": "YmjgZM06jVWrbGnOuUfTItMMZx22",
            "buyer_info": {
                "email": "lucas@gmail.com",
                "username": "Lucas"
            },
            "buyer_location": {
                "latitude": -34.6,
                "longitude": -58.5
            },
            "has_to_be_shipped": False,
            "payment_info": {
                "card_number": "1234-1322-1223-1223",
                "cardholder_name": "Pepe Gutierrez",
                "expiration_date": "01/22",
                "payment_method": "Mastercard",
                "security_code": "123"
            },
            "product_id": "5bd7b28bc9133f00087dd8e8",
            "product_location": {
                "latitude": -34.558499,
                "longitude": -58.466767
            },
            "product_name": "Placa de video ATI 5750",
            "products_total": 450000,
            "seller": "YmjgZM06yVWrbGnuUfTIo9MZx28",
            "seller_info": {
                "email": "lucas@gmail.com",
                "username": "Lucas Hemmingsen"
            },
            "shipping_cost": 1000,
            "status": "PAGO PENDIENTE DE PROCESO",
            "total": 451000,
            "tracking_number": 148,
            "units": 15
        }

        self.order_without_delivery_and_payed = {
            "_id": "5c107700e3c00c56a904cb9b",
            "buyer": "YmjgZM06jVWrbGnOuUfTItMMZx22",
            "buyer_info": {
                "email": "lucas@gmail.com",
                "username": "Lucas"
            },
            "buyer_location": {
                "latitude": -34.6,
                "longitude": -58.5
            },
            "has_to_be_shipped": False,
            "payment_info": {
                "card_number": "1234-1322-1223-1223",
                "cardholder_name": "Pepe Gutierrez",
                "expiration_date": "01/22",
                "payment_method": "Mastercard",
                "security_code": "123"
            },
            "product_id": "5bd7b28bc9133f00087dd8e8",
            "product_location": {
                "latitude": -34.558499,
                "longitude": -58.466767
            },
            "product_name": "Placa de video ATI 5750",
            "products_total": 450000,
            "seller": "YmjgZM06yVWrbGnuUfTIo9MZx28",
            "seller_info": {
                "email": "lucas@gmail.com",
                "username": "Lucas Hemmingsen"
            },
            "shipping_cost": 1000,
            "status": "PAGO ACEPTADO",
            "total": 451000,
            "tracking_number": 148,
            "units": 15
        }

    def get_order_with_delivery_and_not_shipped(self):
        return OrderSchema().load(self.order_with_delivery_and_not_shipped)

    def get_order_with_delivery_and_shipped(self):
        return OrderSchema().load(self.order_with_delivery_and_shipped)

    def get_order_without_delivery_and_not_payed(self):
        return OrderSchema().load(self.order_without_delivery_and_not_payed)

    def get_order_without_delivery_and_payed(self):
        return OrderSchema().load(self.order_without_delivery_and_payed)


class ProductData(Data):
    def __init__(self):
        Data.__init__(self)
        self.product_id = "5bbe37a1e3c00c493839d19e"
        self.question_id = "5bbe37a1e3c00d493439d19e"
        self.category_id = "5bbe37a1e3c00d493439d19e"
        self.valid_product = {
            "_id": "5bd7b28bc9133f00087dd8e8",
            "name": "Placa de video ATI 5750",
            "published": "2018-10-30 01:23:23.152590",
            "pictures": [
                "https://www.amd.com/PublishingImages/photography/product/360px/ATI-Radeon-HD-5750.png"
            ],
            "price": 30000,
            "payment_methods": [
                {
                    "type": 0,
                    "name": "Efectivo",
                    "image": "http://soloefectivo.com.ar/image.jpg"
                },
                {
                    "type": 1,
                    "name": "Visa",
                    "image": "https://firebasestorage.googleapis.com/v0/b/comprameli-49a1b.appspot.com/o/images%2Fpayments%2Fvisa.png?alt=media&token=fed5389f-a966-4f22-82e9-0181784667a7"
                },
                {
                    "type": 1,
                    "name": "American Express",
                    "image": "https://firebasestorage.googleapis.com/v0/b/comprameli-49a1b.appspot.com/o/images%2Fpayments%2Famex.png?alt=media&token=70c950b6-a60e-4bc3-85ee-fb8cb5d4b82b"
                },
                {
                    "type": 1,
                    "name": "Mastercard",
                    "image": "https://firebasestorage.googleapis.com/v0/b/comprameli-49a1b.appspot.com/o/images%2Fpayments%2Fmastercard.png?alt=media&token=0deb3fdc-db7b-464a-9f0a-f7c4126808f6"
                }
            ],
            "seller": "YmjgZM06jVWrbGnOuUfTItMMZx22",
            "categories": [
                "tecnologia"
            ],
            "description": "Placa de video para gamers",
            "location": {
                "longitude": -58.466767,
                "latitude": -34.558499
            },
            "units": 3
        }

        self.valid_product_from_other_user_than_valid_token_header = {
            "_id": "5bd7503ce3c00c227004742b",
            "categories": [
                "mesa",
                "usado",
                "rectangular"
            ],
            "description": "Mesa Cuadrada",
            "location": {
                "longitude": 25.2084,
                "latitude": 55.2719
            },
            "name": "Mesa",
            "payment_methods": [
                {
                    "name": "visa",
                    "type": 1,
                    "image": "http://visa.com.ar/image.jpg"
                },
                {
                    "name": "amex",
                    "type": 1,
                    "image": "http://amex.com.ar/image.jpg"
                }
            ],
            "pictures": [
                "https://www.mesas.com/1.jpg",
                "https://www.mesas.com/2.jpg",
                "https://www.mesas.com/3.jpg"
            ],
            "price": 543.32,
            "published": "2018-10-29 15:23:56.443754",
            "seller": "YmjgZM06jVWrbGnOu45fTItMMZx22",
            "units": 12
        }

        self.product_with_3_units = {
            "_id": "5bd7b28bc9133f00087dd8e8",
            "name": "Placa de video ATI 5750",
            "published": "2018-10-30 01:23:23.152590",
            "pictures": [
                "https://www.amd.com/PublishingImages/photography/product/360px/ATI-Radeon-HD-5750.png"
            ],
            "price": 30000,
            "payment_methods": [
                {
                    "type": 0,
                    "name": "Efectivo",
                    "image": "http://soloefectivo.com.ar/image.jpg"
                },
                {
                    "type": 1,
                    "name": "Visa",
                    "image": "https://firebasestorage.googleapis.com/v0/b/comprameli-49a1b.appspot.com/o/images%2Fpayments%2Fvisa.png?alt=media&token=fed5389f-a966-4f22-82e9-0181784667a7"
                },
                {
                    "type": 1,
                    "name": "American Express",
                    "image": "https://firebasestorage.googleapis.com/v0/b/comprameli-49a1b.appspot.com/o/images%2Fpayments%2Famex.png?alt=media&token=70c950b6-a60e-4bc3-85ee-fb8cb5d4b82b"
                },
                {
                    "type": 1,
                    "name": "Mastercard",
                    "image": "https://firebasestorage.googleapis.com/v0/b/comprameli-49a1b.appspot.com/o/images%2Fpayments%2Fmastercard.png?alt=media&token=0deb3fdc-db7b-464a-9f0a-f7c4126808f6"
                }
            ],
            "seller": "YmjgZM06jVWrbGnOuUfTItMMZx23",
            "categories": [
                "tecnologia"
            ],
            "description": "Placa de video para gamers",
            "location": {
                "longitude": -58.466767,
                "latitude": -34.558499
            },
            "units": 3
        }

        self.invalid_product = {
            "name": "Mesa",
            "description": "Mesa Cuadrada",
            "seller": "YmjgZM06jVWrbGnOuUfTItMMZx22",
            "units": 12
        }

        self.valid_answer = {
            "answer": "Esta es una respuesta valida"
        }

        self.invalid_answer = {
            "respuesta": "Esta es una respuesta invalida"
        }

        self.invalid_question = {
            "pregunta": "Esta es una pregunta invalida?"
        }

        self.valid_question = {
            "question": "Esta es una pregunta valida?"
        }

        self.several_valid_products = [
            {
                "_id": "5bbe37a1e3c00c493839d19e",
                "categories": [
                    "mesa",
                    "usado",
                    "rectangular"
                ],
                "description": "Mesa rectangular",
                "location": {
                    "longitude": 25.2084,
                    "latitude": 55.2719
                },
                "name": "Mesa",
                "payment_methods": [
                    {
                        "name": "visa",
                        "type": 1,
                        "image": "http://visa.com.ar/image.jpg"
                    },
                    {
                        "name": "amex",
                        "type": 1,
                        "image": "http://amex.com.ar/image.jpg"
                    }
                ],
                "pictures": [
                    "https://www.mesas.com/1.jpg",
                    "https://www.mesas.com/2.jpg",
                    "https://www.mesas.com/3.jpg"
                ],
                "price": 543.32,
                "published": "2018-10-10 14:32:17.671122",
                "seller": "YmjgZM06jVWrbGnOuUfTItMMZx22",
                "units": 12
            },
            {
                "_id": "5bbe3a84e3c00c4c29ee6150",
                "categories": [
                    "mesa",
                    "usado",
                    "rectangular"
                ],
                "description": "Mesa Cuadrada",
                "location": {
                    "longitude": 25.2084,
                    "latitude": 55.2719
                },
                "name": "Mesa",
                "payment_methods": [
                    {
                        "name": "visa",
                        "type": 1,
                        "image": "http://visa.com.ar/image.jpg"
                    },
                    {
                        "name": "amex",
                        "type": 1,
                        "image": "http://amex.com.ar/image.jpg"
                    }
                ],
                "pictures": [
                    "https://www.mesas.com/1.jpg",
                    "https://www.mesas.com/2.jpg",
                    "https://www.mesas.com/3.jpg"
                ],
                "price": 543.32,
                "published": "2018-10-10 14:44:36.583794",
                "seller": "YmjgZM06jVWrbGnOuUfTItMMZx22",
                "units": 12
            }
        ]

        self.invalid_input_category = {
            "nombre": "categoria"
        }

        self.valid_input_category = {
            "name": "categoria"
        }

        self.empty_input_category = {
            "name": ""
        }

    def get_products_return_value(self):
        return self.several_valid_products

    def get_product_with_3_units(self):
        schema = ProductSchema()
        return schema.load(self.product_with_3_units)

    def get_valid_product_from_other_user_than_valid_token_header(self):
        schema = ProductSchema()
        return schema.load(self.valid_product_from_other_user_than_valid_token_header)

    def get_valid_product(self):
        schema = ProductSchema()
        return schema.load(self.valid_product)


class PaymentMethodData(Data):
    def __init__(self):
        Data.__init__(self)
        self.valid_payment_method = {
            "name": "visa",
            "type": 1,
            "image": "http://visa.com.ar/logo.jpg"
        }

    def get_valid_payment_method(self):
        schema = PaymentMethodSchema()
        return schema.load(self.valid_payment_method)


class UserData(Data):
    def __init__(self):
        Data.__init__(self)
        self.uid = 'YmjgZM06jVWrbGnOuUfTItMMZx22'
        self.valid_user = {
            "_id": "5bca2c83e3c00c74104dd7c2",
            "photo": "https://www.iemoji.com/view/emoji/1336/skin-tones/man-medium-skin-tone",
            "member_since": "2018-10-19 16:12:03.159657",
            "google": "nombre@gmail.com",
            "facebook": "123342342342",
            "email": "nombre@gmail.com",
            "uid": "YmjgZM06jVWrbGnOuUfTIo9MZx22",
            "last_login": "2018-10-19 16:12:03.159685",
            "surname": "Apellido",
            "name": "Nombre",
            "location": {
                "longitude": -58.482608,
                "latitude": -34.5831
            },
            "points": 106,
            "purchases": 15
        }
        self.invalid_user = {
            "email": "nombre@gmail.com",
            "facebook": "123342342342",
            "google": "nombre@gmail.com",
            "name": "Nombre",
            "photo": "https://www.iemoji.com/view/emoji/1336/skin-tones/man-medium-skin-tone",
            "surname": "Apellido",
            "age": 28
        }

    def get_valid_user(self):
        return UserSchema().load(self.valid_user)



@pytest.fixture
def client():
    app = appserver.app.create_app(TestingConfig)
    test_client = app.test_client()
    yield test_client


@pytest.fixture
def product_data():
    yield ProductData()


@pytest.fixture
def user_data():
    yield UserData()


@pytest.fixture
def order_data():
    yield OrderData()

@pytest.fixture
def payment_method_data():
    yield PaymentMethodData()
