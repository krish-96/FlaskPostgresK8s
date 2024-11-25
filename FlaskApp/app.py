import os
from flask import Flask, render_template_string, url_for

from FlaskApp.database import get_connection
from FlaskApp.exceptions import UnableToConnect
from FlaskApp.log_configs import logger
from FlaskApp.utils import (
    check_platform_compatibility, get_server_properties, check_db_status,
    get_current_version, get_current_release_notes, get_all_releases
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    logger.debug("User Accessed Home page")
    return render_template_string(
        f"""
        You can start using the application, 
        Everything is working fine.
        <br/>Use below urls to access:
        <br/><a href="{url_for("db_connection_check")}" target="_blank">DB status</a>
        <br/><a href="{url_for("get_current_release")}" target="_blank">Current Release</a>
        <br/><a href="{url_for("get_current_release_version")}" target="_blank">Current Release Version</a>
        <br/><a href="{url_for("get_releases")}" target="_blank">All Releases</a>
        """
    )


@app.route("/is_db_alive", methods=["GET"])
def db_connection_check():
    logger.debug("User Accessed DB Connection Check page")
    return dict(
        status=True if check_db_status() else False
    )


@app.route("/current_release", methods=["GET"])
def get_current_release():
    logger.debug("User Accessed Current Release Page")
    release_details = get_current_release_notes()
    return dict(
        currentRelease=release_details[0] if release_details and isinstance(release_details, list) else release_details
    )


@app.route("/current_release_version", methods=["GET"])
def get_current_release_version():
    logger.debug("User Accessed Current Release Version Page")
    return dict(
        currentVersion=get_current_version()
    )


@app.route("/releases", methods=["GET"])
def get_releases():
    logger.debug("User Accessed Releases Page")
    return dict(
        releases=get_all_releases()
    )


def start_app():
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
                if use_env_variables not in (True, 'True', 'true', 1):
                    host = str(server_props['host'])
                    port = server_props['port']
                    debug = server_props['debug']
                else:
                    logger.debug("Server properties are given in the environment variables")
                    host = os.getenv('host')
                    port = os.getenv('port')
                    debug = os.getenv('debug') or False

                # print(f"host: {host} port: {port} debug: {debug}")

                # For local developement
                # app.run(host="0.0.0.0", port=6000, debug=debug, use_reloader=use_reloader)
                logger.debug("Starting the app")
                app.run(host=host, port=port, debug=debug)
            logger.debug("Server properties are not available!")
    except Exception as start_app_err:
        logger.error(f"Exception occurred while starting the app, Exception: {start_app_err}")


if __name__ == "__main__":
    start_app()
