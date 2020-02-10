from enum import IntEnum, unique


@unique
class ErrorCodes(IntEnum):
    """
    class to store different error codes
    """

    def __new__(cls, value, description):
        obj = int.__new__(cls, value)

        obj._value_ = value
        obj.description = description

        return obj

    API_NOT_FOUND = (100, 'API not found')
    METHOD_NOT_ALLOWED = (200, 'Method not allowed')
