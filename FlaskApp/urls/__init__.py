from .release import release_ns
from .database import database_ns
from .user import user_ns, user_blueprint

flask_app_namespaces = [release_ns, database_ns, user_ns]
flask_app_blueprints = [user_blueprint]
