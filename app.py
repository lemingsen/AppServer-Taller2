"""Initial config and routing."""
from flask import Flask
from api import blueprint as api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)
