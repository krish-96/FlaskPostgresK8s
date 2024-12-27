import os
from typing import Dict
from .db_constants import psql_uri, mongo_uri
from FlaskApp.log_configs import logger
from FlaskApp.exceptions import DataBaseDetailsNotFound

# Module constants
MISSING_DB_DETAILS = "Missing DB details!"
NO_DB_SPECIFIED = "Database type not specified to get the URI!"

POSTGRES = "postgres"
MONGO = "mongo"

DB_CONFIGS_AVAILABLE_FOR = frozenset([POSTGRES, MONGO])


class _PostgresDatabaseConfigs:
    """
    This class contains the postgres database configuration
    """
    @classmethod
    def _get_psql_db_details(cls) -> Dict:
        """Fetches PostgreSQL database details."""
        try:
            db_details = dict(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                name=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
            )
            db_details = {k: int(v) if v and v.isdigit() else v.strip() if isinstance(v, str) else v
                          for k, v in db_details.items()}
            return db_details
        except Exception as err:
            logger.critical(f"Error fetching PostgreSQL details: {err}")
            raise err

    @classmethod
    def _get_psql_db_name(cls) -> Dict:
        """Fetches PostgreSQL database details."""
        try:
            return cls._get_psql_db_details()['name']
        except Exception as err:
            logger.critical(f"Error fetching PostgreSQL database name: {err}")
            raise err

    @classmethod
    def _get_psql_db_uri(cls) -> str:
        """Generates PostgreSQL connection URI."""
        try:
            db_details = cls._get_psql_db_details()
            if not db_details:
                raise DataBaseDetailsNotFound(MISSING_DB_DETAILS)
            return psql_uri.format(
                user=db_details["user"],
                password=db_details["password"],
                host=db_details["host"],
                port=int(db_details["port"]),
                dbname=db_details["name"],
            )
        except Exception as err:
            logger.critical(f"Error generating PostgreSQL URI: {err}")
            raise err


class _MongoDatabaseConfigs:
    """
    This class contains the mongo database configuration
    """
    @classmethod
    def _get_mongo_db_details(cls) -> Dict:
        """Fetches MongoDB database details."""
        try:
            db_details = dict(
                host=os.getenv("MDB_HOST"),
                port=os.getenv("MDB_PORT"),
                name=os.getenv("MDB_NAME"),
                user=os.getenv("MDB_USER"),
                password=os.getenv("MDB_PASS"),
                authentication_database=os.getenv("MAUTHENTICATION_DATABASE"),
            )
            db_details = {k: int(v) if v and v.isdigit() else v.strip() if isinstance(v, str) else v
                          for k, v in db_details.items()}
            return db_details
        except Exception as err:
            logger.critical(f"Error fetching MongoDB details: {err}")
            raise err

    @classmethod
    def _get_mongo_db_name(cls) -> Dict:
        """Fetches Mongo database details."""
        try:
            return cls._get_mongo_db_details()['name']
        except Exception as err:
            logger.critical(f"Error fetching Mongo database name: {err}")
            raise err

    @classmethod
    def _get_mongo_db_uri(cls) -> str:
        """Generates MongoDB connection URI."""
        try:
            db_details = cls._get_mongo_db_details()
            if not db_details:
                raise DataBaseDetailsNotFound(MISSING_DB_DETAILS)
            return mongo_uri.format(
                user=db_details["user"],
                password=db_details["password"],
                host=db_details["host"],
                port=db_details["port"],
                dbname=db_details["name"],
                authentication_database=db_details.get(
                    "authentication_database"
                ) if db_details.get("authentication_database") else "admin"
            )
        except Exception as err:
            logger.critical(f"Error generating MongoDB URI: {err}")
            raise err


class DatabaseConfigs(_PostgresDatabaseConfigs, _MongoDatabaseConfigs):
    """
    This is a wrapper class to fetch the database configuration
    """
    def __init__(self, db_type, fetch_uri=False, fetch_name=False):
        self.details_for = db_type
        self.fetch_uri = fetch_uri
        self.fetch_name = fetch_name
        if (self.fetch_uri or self.fetch_name) and not self.details_for:
            logger.critical(NO_DB_SPECIFIED)
            raise ValueError(NO_DB_SPECIFIED)

    def get(self):
        """
        This method will return the requested database details, based on the object created
        If the object created to get the database uri, then it'll return the database uri
        If the object created to get the database name, then it'll return the database name
        else it'll return the database details
        :return:
        """
        if self.fetch_uri:
            if self.details_for == POSTGRES:
                return self._get_psql_db_uri()
            else:
                return self._get_mongo_db_uri()
        elif self.fetch_name:
            if self.details_for == POSTGRES:
                return self._get_psql_db_name()
            else:
                return self._get_mongo_db_name()
        else:
            if self.details_for == POSTGRES:
                return self._get_psql_db_details()
            else:
                return self._get_mongo_db_details()
