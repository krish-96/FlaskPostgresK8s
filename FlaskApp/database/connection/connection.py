import psycopg2
import sqlalchemy.engine
from sqlalchemy import create_engine
from pymongo import mongo_client

from FlaskApp.log_configs import logger

from .configs import DatabaseConfigs, POSTGRES, MONGO, DB_CONFIGS_AVAILABLE_FOR


def __get_db_configs(db_type=POSTGRES, fetch_uri=False, fetch_name=False):
    if db_type not in DB_CONFIGS_AVAILABLE_FOR:
        raise ValueError(f'db_name must be one of {DB_CONFIGS_AVAILABLE_FOR}!')
    return DatabaseConfigs(db_type=db_type, fetch_uri=fetch_uri, fetch_name=fetch_name).get()


def get_psql_uri():
    """This function will return the psql database uri"""
    return __get_db_configs(db_type=POSTGRES, fetch_uri=True)


def get_sql_db_name() -> str | None:
    """This function will return the name of the sql database"""
    return __get_db_configs(db_type=POSTGRES, fetch_name=True)


def get_mongo_db_name() -> str | None:
    """This function will return the name of the mongo database"""
    return __get_db_configs(db_type=MONGO, fetch_name=True)


def get_mongo_client() -> mongo_client.MongoClient:
    """This function will return the mongo client"""
    # mongo_client.MongoClient("localhost", 27017)
    mongo_db_uri = __get_db_configs(db_type=MONGO, fetch_uri=True)
    mongo_client_obj = mongo_client.MongoClient(mongo_db_uri)
    return mongo_client_obj


__MONGO_CON = None
import threading
lock = threading.Lock()

def _get_mongo_connection() -> mongo_client.database.Database:
    """This function will return the database connection from the mongo client"""
    try:
        # client = get_mongo_client()
        # mongo_db_name = get_mongo_db_name()
        # return client.get_database(mongo_db_name)

        global __MONGO_CON
        with lock:
            # get_mongo_client()
            # mongo_db_name = get_mongo_db_name()
            __MONGO_CON = get_mongo_client()
        # if __MONGO_CON is None:
        #     with lock:
        #         if __MONGO_CON is None:
        #             client = get_mongo_client()
        #             mongo_db_name = get_mongo_db_name()
        #             __MONGO_CON = client.get_database(mongo_db_name)
        return __MONGO_CON
    except Exception as con_err:
        print(f"Exception occurred while fetching the DB connection, Exception: {con_err}")

def get_mongo_connection() -> mongo_client.database.Database:
    """This function will return the database connection from the mongo client"""
    try:
        client = get_mongo_client()
        mongo_db_name = get_mongo_db_name()
        return client.get_database(mongo_db_name)
        # return _get_mongo_connection()
    except Exception as con_err:
        print(f"Exception occurred while fetching the DB connection, Exception: {con_err}")


def get_connection() -> psycopg2.connect:
    """This function will return the psql database connection"""
    try:
        db_details = __get_db_configs(db_type=POSTGRES)
        if db_details:
            # we set database name as name in the db details
            # But psycopg2 requires database key, instead of name
            db_details['database'] = db_details['name']
            del db_details['name']
        return psycopg2.connect(**db_details)
    except Exception as con_err:
        logger.error(f"Exception occurred while fetching the DB connection, Exception: {con_err}")


def get_engine() -> sqlalchemy.engine.Engine.connect:
    """This function will return the psql database engine connection"""
    try:
        engine = create_engine(get_psql_uri())
        engine_connection = engine.connect()
        return engine_connection
    except Exception as con_err:
        print(f"Exception occurred while fetching the DB connection, Exception: {con_err}")
