import os
import psutil
from sys import prefix

from flask import Flask, render_template_string

from FlaskApp.restx import api
from FlaskApp.log_configs import logger
from FlaskApp.utils import (
    check_platform_compatibility, get_server_properties, check_db_status
)
from FlaskApp.database import SetTestDataBase
from FlaskApp.exceptions import UnableToConnect
from FlaskApp.scheduler_configs import Scheduler
from FlaskApp.request_handlers import SchedulerJobs
from FlaskApp.routes import flask_app_blueprints, flask_app_namespaces

app = Flask(__name__)


@app.route("/home", methods=["GET"])
def index():
    logger.debug("User Accessed Home page")
    return render_template_string(
        """
        You can start using the application, 
        Everything is working fine.
        <br/>Use below routes to access:
        <br/><a href="/db/status" target="_blank">DB status</a>
        <br/><a href="/release/current_release" target="_blank">Current Release</a>
        <br/><a href="/release/current_release_version" target="_blank">Current Release Version</a>
        <br/><a href="/release/releases" target="_blank">All Releases</a>
        """
    )


def initialize_app(flaskapp) -> None:
    """This function will initialize the flask app with Flask restx Api"""
    logger.info("Initializing the flaskapp with flask restx is started")
    api.init_app(flaskapp)
    logger.info("Initializing the flaskapp with flask restx is successful")


def initialize_namespaces() -> None:
    """This function will initialize the flask app namespaces"""
    logger.info("Initializing the flaskapp namespaces is started")
    for ns in flask_app_namespaces:
        # In the latest flask_restx, noticed that whenever new namespace space is created, it's adding automatically
        # Adding means registering
        # So we are registering the namespace, if it's not available
        if ns not in api.namespaces:
            api.add_namespace(ns, path=f"/api/{ns.name}" if 'api/' not in ns.name else ns.name )
    logger.debug("Initializing the flaskapp namespaces is successful")


def initialize_blueprints() -> None:
    """This function will initialize the flask app blueprints"""
    logger.info("Initializing the flaskapp blueprints is started")
    for bp in flask_app_blueprints:
        if bp not in app.blueprints:
            app.register_blueprint(bp)
    logger.debug("Initializing the flaskapp blueprints is successful")


def set_up_test_tables() -> None:
    """This function will set up the test tables in the database"""
    logger.info("Setting up the test tables in the database")
    set_test_db_obj = SetTestDataBase()
    if not set_test_db_obj.set_test_tables():
        set_test_db_obj.set_test_data()
    set_test_db_obj.verify_test_data()
    logger.info("Setting up the test tables in the database is successful")


def setup_scheduler_jobs() -> None:
    """This function will set up the test tables in the database"""
    logger.info("Setting up the scheduler")
    scheduler = Scheduler()
    scheduler.setup_scheduler()
    scheduler.start_jobs()
    SchedulerJobs().add_scheduler_basic_jobs()
    logger.info("Setting up the scheduler is successful")

def monitor_memory():
    mem = psutil.virtual_memory()
    logger.debug(f"Memory usage: {mem.percent}% ({mem.used} of {mem.total})")

@app.before_request
def log_memory_usage():
    monitor_memory()

def start_app() -> None:
    """This function will check for the necessary details for the app and start"""
    try:
        logger.debug("Checking the compatibility of the platform")
        if check_platform_compatibility():
            logger.debug("App will support the Current platform")
            logger.debug("Checking the Database status")
            is_db_connected = check_db_status()
            if not is_db_connected:
                logger.debug("App cannot utilize Database i.e., Database is down or connectivity issue")
                raise UnableToConnect("Unable to Connect to the Database")
            logger.debug("App can utilize Database i.e., Database is up and running")
            server_props = get_server_properties()
            if not server_props:
                logger.info("Server properties are not available!")
                raise ValueError("Server properties are not available")
            logger.debug("Server properties are available")
            use_env_variables = server_props['use_env_variables']
            enabled_flogs = frozenset([True, 'True', 'true', 1])
            if use_env_variables not in enabled_flogs:
                host = str(server_props['host'])
                port = server_props['port']
                debug = server_props['debug']
            else:
                logger.debug("Server properties are given in the environment variables")
                host = os.getenv('host')
                port = os.getenv('port')
                debug = os.getenv('debug') or False

            debug = True if debug in enabled_flogs else False

            # print(f"host: {host} port: {port} debug: {debug}")

            # For local development
            # app.run(host="0.0.0.0", port=5000, debug=debug, use_reloader=use_reloader)
            logger.debug("Running the initials before Starting the app")

            initialize_app(app)
            initialize_namespaces()
            initialize_blueprints()
            set_up_test_tables()
            setup_scheduler_jobs()

            logger.debug("Starting the app")
            # if __name__ == '__main__':
            app.run(host=host, port=port, debug=True)
            # else:
            #     return app
            # return app
            logger.debug("App is ready to be served by Gunicorn.")

            logger.debug("Stopping the app")


    except Exception as start_app_err:
        logger.error(f"Exception occurred while starting the app, Exception: {start_app_err}")
        import sys
        err_type, err_value, err_traceback = sys.exc_info()
        tb_line_no = err_traceback.tb_lineno
        logger.error(f"Exact Exception @ {tb_line_no} {err_type} {err_value} {tb_line_no}")


if __name__ == "__main__":
    start_app()
