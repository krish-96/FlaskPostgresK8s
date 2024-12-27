from .platform import UnSupportedPlatform
from .generic import UnableToConnect
from .database import (
    TableNameIsRequired, QueryIsRequired, DeleteQueryWithOutWhereNotAllowed, DropQueryNotAllowed,
    DataBaseConnectionFailed, DataBaseDetailsNotFound
)
