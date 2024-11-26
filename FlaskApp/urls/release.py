from flask_restx.namespace import Namespace
from flask_restx import Resource

from FlaskApp.log_configs import logger
from FlaskApp.utils import get_current_release_notes, get_current_version, get_all_releases

__all__ = ['release_ns']

release_ns = Namespace('release', prefix="api", description="A namespace to hole all the release endpoints")


@release_ns.route("/current_release")
class CurrentRelease(Resource):
    def get(self):
        logger.debug("User Accessed Current Release Page")
        release_details = get_current_release_notes()
        return dict(
            currentRelease=release_details[0] if release_details and isinstance(release_details,
                                                                                list) else release_details
        )


@release_ns.route("/current_release_version")
class CurrentReleaseVersion(Resource):
    def get(self):
        logger.debug("User Accessed Current Release Version Page")
        return dict(
            currentVersion=get_current_version()
        )


@release_ns.route("/releases")
class Releases(Resource):
    def get(self):
        logger.debug("User Accessed Releases Page")
        return dict(
            releases=get_all_releases()
        )
