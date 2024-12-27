from flask import Blueprint, request
from FlaskApp.restx import api
from flask_restx import Resource

from FlaskApp.log_configs import logger
from FlaskApp.database.handler import UserHandler

__all__ = ['user_ns', 'user_blueprint']

user_blueprint = Blueprint('user', __name__, url_prefix='/user')
user_ns = api.namespace('api/user', description="A namespace to hold all the user endpoints")


@user_blueprint.route('/')
def user_home():
    return """<h1>I'll deal with users</h1>"""


@user_ns.route('/list')
class Users(Resource):
    def get(self):
        users = UserHandler().get_users()
        logger.debug(f"Received user: {users}")
        return dict(users=users)


@user_ns.route('/create')
@user_ns.param('username', 'username')
class CreateUser(Resource):
    def post(self):
        username = request.args.get('username')
        logger.debug(f"Received username from request: {username}")
        user_details = UserHandler().create_user(username=username)
        logger.debug(f"Received user details: {user_details}")
        return dict(user=user_details)


@user_ns.route('/details')
@user_ns.param('id', 'The User ID')
class CreateDetails(Resource):
    def get(self):
        user_id = request.args.get('id')
        logger.debug(f"Received user Id from request: {user_id}")
        user_details = UserHandler().get_user(user_id)
        logger.debug(f"Received user details: {user_details}")
        return dict(user=user_details)
