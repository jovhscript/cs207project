import enum

class TSDBError(Exception):
    """Base class for exceptions in this module."""
    pass

class TSDBOperationError(TSDBError):
    """
    Exception thrown when an error occurs while performing
    operations on timeseries objects.
    """

    pass

class TSDBInputError(TSDBError):
    """
    Exception thrown when there is a problem with an input
    in the client request.
    """
    pass

class TSDBStorageError(TSDBError):
    """
    Exception thrown when file missing from the database storage.
    """
    pass

class TSDBConnectionError(TSDBError):
    """
    Exception thrown when there is an error in the connection
    between the client and the server.
    """
    pass
