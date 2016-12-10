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

class TSDBStatus(enum.IntEnum):
    OK = 0
    UNKNOWN_ERROR = 1
    INVALID_OPERATION = 2
    INVALID_KEY = 3
    INVALID_COMPONENT = 4

    @staticmethod
    def encoded_length():
        return 3

    def encode(self):
        return str.encode('{:3d}'.format(self.value))

    @classmethod
    def from_bytes(cls, data):
        return cls(int(data.decode()))
