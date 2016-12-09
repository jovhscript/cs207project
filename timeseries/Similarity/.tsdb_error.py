import enum

class TSDBError(Exception):
    """Base class for exceptions in this module."""
    pass

class TSDBOperationError(TSDBError):
    pass

class TSDBConnectionError(TSDBError):
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
