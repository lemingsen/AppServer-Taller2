import pytest
import appserver
from config import TestingConfig


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


class ProductData(Data):
    def __init__(self):
        Data.__init__(self)
        self.product_id = "5bbe37a1e3c00c493839d19e"
        self.valid_product = {
            "_id": "5bd7503ce3c00c227004742b",
            "categories": [
                "mesa",
                "usado",
                "rectangular"
            ],
            "description": "Mesa Cuadrada",
            "location": {
                "x": 25.2084,
                "y": 55.2719
            },
            "name": "Mesa",
            "payment_methods": [
                "visa",
                "amex",
                "bitcoin"
            ],
            "pictures": [
                "https://www.mesas.com/1.jpg",
                "https://www.mesas.com/2.jpg",
                "https://www.mesas.com/3.jpg"
            ],
            "price": 543.32,
            "published": "2018-10-29 15:23:56.443754",
            "seller": "YmjgZM06jVWrbGnOuUfTItMMZx22",
            "units": 12
        }

        self.invalid_product = {
            "name": "Mesa",
            "description": "Mesa Cuadrada",
            "seller": "YmjgZM06jVWrbGnOuUfTItMMZx22",
            "units": 12
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
                    "x": 25.2084,
                    "y": 55.2719
                },
                "name": "Mesa",
                "payment_methods": [
                    "visa",
                    "amex",
                    "bitcoin"
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
                    "x": 25.2084,
                    "y": 55.2719
                },
                "name": "Mesa",
                "payment_methods": [
                    "visa",
                    "amex",
                    "bitcoin"
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

    def get_products_return_value(self):
        return self.several_valid_products


class UserData(Data):
    def __init__(self):
        Data.__init__(self)
        self.uid = 'YmjgZM06jVWrbGnOuUfTItMMZx22'
        self.valid_user = {
            "email": "nombre@gmail.com",
            "facebook": "123342342342",
            "google": "nombre@gmail.com",
            "name": "Nombre",
            "photo": "https://www.iemoji.com/view/emoji/1336/skin-tones/man-medium-skin-tone",
            "surname": "Apellido",
            "uid": "YmjgZM06yVWrbGnOuUfTIo9MZx22"
        }
        self.invalid_user = {
            "email": "nombre@gmail.com",
            "facebook": "123342342342",
            "google": "nombre@gmail.com",
            "name": "Nombre",
            "photo": "https://www.iemoji.com/view/emoji/1336/skin-tones/man-medium-skin-tone",
            "surname": "Apellido"
        }




@pytest.fixture
def client():
    app = appserver.create_app(TestingConfig)
    test_client = app.test_client()
    yield test_client


@pytest.fixture
def product_data():
    yield ProductData()


@pytest.fixture
def user_data():
    yield UserData()
