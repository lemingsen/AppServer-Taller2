"""Service layer exceptions"""
# pylint: disable=R0401

class NotFoundError(Exception):
    """Raised when a resource is not found."""
    def __init__(self, message):
        super(NotFoundError, self).__init__(message)
        self.message = message


class UserExistsError(Exception):
    """Raised when trying to register an already existent user"""
    def __init__(self):
        message = "User already exists."
        super(UserExistsError, self).__init__(message)
        self.message = message
