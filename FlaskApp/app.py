import os
from flask import Flask, render_template_string, url_for

from FlaskApp.restx import api
from FlaskApp.log_configs import logger
from FlaskApp.utils import (
    check_platform_compatibility, get_server_properties, check_db_status
)

from FlaskApp.exceptions import UnableToConnect

from FlaskApp.urls import flask_app_blueprints, flask_app_namespaces

app = Flask(__name__)


@app.route("/home", methods=["GET"])
def index():
    logger.debug("User Accessed Home page")
    return render_template_string(
        """
        You can start using the application, 
        Everything is working fine.
        <br/>Use below urls to access:
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
    # api.add_namespace()
    logger.info("Initializing the flaskapp with flask restx is successful")


def initialize_namespaces() -> None:
    """This function will initialize the flask app namespaces"""
    logger.info("Initializing the flaskapp namespaces is started")
    for ns in flask_app_namespaces:
        api.add_namespace(ns)
    logger.debug("Initializing the flaskapp namespaces is successful")


def initialize_blueprints() -> None:
    """This function will initialize the flask app blueprints"""
    logger.info("Initializing the flaskapp blueprints is started")
    for bp in flask_app_blueprints:
        app.register_blueprint(bp)
    logger.debug("Initializing the flaskapp blueprints is successful")


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
            if server_props:
                logger.debug("Server properties are available")
                use_env_variables = server_props['use_env_variables']
                enabled_flogs = {True, 'True', 'true', 1}
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

                logger.debug("Starting the app")
                app.run(host=host, port=port, debug=debug)
            logger.debug("Server properties are not available!")
    except Exception as start_app_err:
        logger.error(f"Exception occurred while starting the app, Exception: {start_app_err}")


if __name__ == "__main__":
    start_app()
