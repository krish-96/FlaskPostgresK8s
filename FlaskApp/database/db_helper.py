from typing import Optional, Dict, List
from sqlalchemy import text
from .connection import get_connection, get_engine
from FlaskApp.log_configs import logger
from FlaskApp.exceptions import (
    QueryIsRequired, TableNameIsRequired, DeleteQueryWithOutWhereNotAllowed, DropQueryNotAllowed
)

QUERY_REQUIRED = "Query is required"
TABLE_NAME_REQUIRED = "Table is required"


def __validate_query(query):
    """
    This function will validate the given query and also for the DELETE and DROP
    If the query is having the below scenarios, it'll raise an exception
        1. DROP queries are not allowed
        2. DELETE queries without WHERE clause are not allowed
    """
    if not query:
        raise QueryIsRequired(QUERY_REQUIRED)
    if 'delete from' in query.lower() and 'where' not in query.lower():
        raise DeleteQueryWithOutWhereNotAllowed("DELETE query is missing WHERE clause!")
    if 'drop' in query.lower():
        raise DropQueryNotAllowed("DROP queries are not allowed!")


def __get_query_results_dict_using_engine(engine, query, **kwargs) -> Optional[List[Dict] | List]:
    """
    This function will execute and returns the result of the query in  list of dictionaries
    Note:
        1. DROP queries are not allowed
        2. DELETE queries without WHERE clause are not allowed
    :param engine: sqlalchemy engine connection object
    :param query: sql query to execute
    :param kwargs: arguments for the query
    :returns: list of dictionaries or empty list
    """
    data = engine.execute(text(query), kwargs)
    columns = data.keys()
    results = [dict(zip(columns, row)) for row in data]
    return results


def get_query_results_dict(query, **kwargs) -> Optional[List[Dict] | List]:
    """
    This function will execute the given query and returns the result of the query in  list of dictionaries
    Note:
        1. DROP queries are not allowed
        2. DELETE queries without WHERE clause are not allowed
    :params query: SQL query to be executed
    :returns: list of dictionaries or empty list
    """
    __validate_query(query)
    connection = get_connection()
    try:
        if kwargs:
            engine = get_engine()
            return __get_query_results_dict_using_engine(engine=engine, query=query, **kwargs)
        cursor = connection.cursor()
        cursor.execute(query)
        columns = [i.name for i in cursor.description]
        data = cursor.fetchall()
        results = [dict(zip(columns, i)) for i in data]
        return results
    except DeleteQueryWithOutWhereNotAllowed as query_exec_err:
        logger.critical(f"Cannot execute DELETE query without WHERE clause, Query: {query}")
        raise query_exec_err
    except DropQueryNotAllowed as query_exec_err:
        logger.critical(f"Cannot execute DROP query, Query: {query}")
        raise query_exec_err
    except Exception as query_exec_err:
        logger.error(f"Exception occurred while executing the query, {query_exec_err}")
    finally:
        connection.close()
    return []


def __execute_and_commit_query_using_engine(engine, query, **kwargs) -> None:
    """
    This function will execute the given query and commit the changes
    :param engine: sqlalchemy engine connection object
    :param query: sql query to execute
    :param kwargs: arguments for the query
    :returns: None
    """
    engine.execute(text(query), kwargs)
    engine.commit()


def execute_and_commit_query(query, **kwargs):
    """This function will execute the given query and commits the changes"""
    __validate_query(query)
    connection = get_connection()
    try:
        if kwargs:
            engine = get_engine()
            return __execute_and_commit_query_using_engine(engine=engine, query=query, **kwargs)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except Exception as query_exec_err:
        logger.error(f"Exception occurred while executing the query, {query_exec_err}")
    finally:
        connection.close()


def check_table(table_name):
    connection = get_connection()
    try:
        if not table_name:
            raise TableNameIsRequired(TABLE_NAME_REQUIRED)
        cursor = connection.cursor()
        cursor.execute(f"select * from {table_name} limit 1;")
        return True
    except Exception as query_exec_err:
        logger.error(f"Exception occurred while executing the query, {query_exec_err}")
        return False
    finally:
        connection.close()
