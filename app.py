"""Initial config and routing."""
from flask import Flask
from api import api

app = Flask(__name__)
api.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
