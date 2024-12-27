from FlaskApp.database import execute_and_commit_query
from FlaskApp.database import get_query_results_dict
from FlaskApp.constants import AppEnum
from FlaskApp.utils import get_properties
from FlaskApp.log_configs import logger


class UserHandler(object):

    @staticmethod
    def get_users():
        logger.info("Fetching the users from the database...")
        user_list_query = get_properties(AppEnum.sql_queries_path.value, section='User', option='list')
        users = get_query_results_dict(user_list_query)
        logger.info("Fetching the users from the database is successful")
        return users

    @staticmethod
    def get_user(user_id):
        logger.info("Fetching the user details from the database...")
        user_list_query = get_properties(AppEnum.sql_queries_path.value, section='User', option='details')
        user_details = get_query_results_dict(user_list_query, user_id=user_id)
        logger.info("Fetching the user details from the database is successful")
        return user_details

    @staticmethod
    def create_user(**kwargs):
        logger.info("Creating the user...")
        user_list_query = get_properties(AppEnum.sql_queries_path.value, section='User', option='create')
        if 'username' in kwargs:
            name = kwargs['username']
        elif 'name' in kwargs:
            name = kwargs['name']
        else:
            name = None
        if name:
            execute_and_commit_query(user_list_query, name=name)
        else:
            return "Unable to create a user, Username is missing!"
        logger.info("Created the user successfully")
        return f"Created the user for {name} successfully"
