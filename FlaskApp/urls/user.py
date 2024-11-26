from flask import Blueprint
from flask_restx import Resource
from flask_restx.namespace import Namespace

__all__ = ['user_ns', 'user_blueprint']

user_blueprint = Blueprint('user', __name__, url_prefix='/user')
user_ns = Namespace(
    'user', prefix='/api', description="A namespace to hold all the user endpoints"
)


@user_blueprint.route('/')
def user_home():
    return """<h1>I'll deal with users</h1>"""


@user_ns.route('/list')
class Users(Resource):
    def get(self):
        return """<h1>I'll get users list</h1>"""


@user_ns.route('/list')
class CreateUser(Resource):
    def post(self):
        return """<h1>User will be created soon!</h1>"""

    def get(self):
        return """<h1>I can add user for you!</h1>"""
