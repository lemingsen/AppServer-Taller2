"""Service layer exceptions"""
# pylint: disable=R0401


class NotFoundError(Exception):
    """Raised when a resource is not found."""
    def __init__(self, message):
        super(NotFoundError, self).__init__(message)
        self.message = message


class DataExistsError(Exception):
    """Raised when trying trying to add existent data"""
    def __init__(self, message):
        super(DataExistsError, self).__init__(message)
        self.message = message


class ForbiddenError(Exception):
    """Raised when a user tries to execute
    an operation he does not have priviliges"""
    def __init__(self, message):
        super(ForbiddenError, self).__init__(message)
        self.message = message


class NotEnoughUnitsError(Exception):
    """Raised when a user tries to buy more
    units of a product that the ones available"""
    def __init__(self, message):
        super(NotEnoughUnitsError, self).__init__(message)
        self.message = message


class ExpiredTokenError(Exception):
    """Expired token exception"""
    pass
