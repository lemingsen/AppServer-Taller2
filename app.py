"""Init config and routing."""
from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)


@api.route('/hello')
class HelloWorld(Resource):
    """Hello World"""
    def get(self):
        """Hello World JSON"""
        return {'hello': 'world'}


if __name__ == '__main__':
    app.run(debug=True)
