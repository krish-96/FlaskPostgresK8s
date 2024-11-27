class DataBaseConnectionFailed(Exception):
    """This exception is raised when app is unable to get a database connection"""


class DeleteQueryWithOutWhereNotAllowed(Exception):
    """This exception is raised when delete query is provided without a WHERE clause"""


class DropQueryNotAllowed(Exception):
    """This exception is raised when drop query is provided"""

class TableNameIsRequired(Exception):
    """This exception is raised when a table name is not provided"""


class QueryIsRequired(Exception):
    """This exception is raised when a query is not provided"""
