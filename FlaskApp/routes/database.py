from flask_restx import Resource

from FlaskApp.restx import api
from FlaskApp.log_configs import logger
from FlaskApp.utils import check_db_status

__all__ = ['database_ns']

database_ns = api.namespace('api/db', description="A namespace to hold all the database endpoints")


@database_ns.route("/is_alive")
class DBConnectionCheck(Resource):
    def get(self):
        logger.debug("User Accessed DB Connection Live or not page")
        return dict(status=True if check_db_status() else False)


@database_ns.route("/status")
class DBConnectionStatus(Resource):
    def get(self):
        logger.debug("User Accessed DB Connection status page")
        return dict(
            message="Database is up and running..." if check_db_status() else "Database is down!",
            status="up" if check_db_status() else "down",
        )
