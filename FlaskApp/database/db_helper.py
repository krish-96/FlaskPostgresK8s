from .connection import get_connection
from FlaskApp.log_configs import logger

QUERY_REQUIRED = "Query is required"


def execute_query(query, connection=None):
    try:
        if not connection:
            connection = get_connection()
        if not query:
            raise Exception(QUERY_REQUIRED)
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as query_exec_err:
        logger.error(f"Exception occurred while executing the query, {query_exec_err}")


def execute_ddl_query(query, connection=None):
    try:
        if not connection:
            connection = get_connection()
        if not query:
            raise Exception(QUERY_REQUIRED)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except Exception as query_exec_err:
        logger.error(f"Exception occurred while executing the query, {query_exec_err}")


def check_table(query, connection=None):
    try:
        if not connection:
            connection = get_connection()
        if not query:
            raise Exception(QUERY_REQUIRED)
        cursor = connection.cursor()
        cursor.execute(query)
        return True
    except Exception as query_exec_err:
        logger.error(f"Exception occurred while executing the query, {query_exec_err}")
        return False
