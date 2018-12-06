"""Base Model"""
# pylint: disable=R0903,C0103


class BaseModel:
    """Base model class"""

    def __init__(self):
        self._id = None

    @property
    def id(self):
        """id property"""
        return self._id

    @id.setter
    def id(self, value):
        """id setter"""
        self._id = value
