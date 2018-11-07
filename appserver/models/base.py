"""Base Model"""
# pylint: disable=R0903,C0103


class BaseModel:
    """Base model class"""
    # schema = None

    def __init__(self):
        self._id = None

    @property
    def id(self):
        """id property"""
        return self._id
    # def to_dict(self):
    #     return self.schema.load(self)
    #
    # def from_dict(self, data):
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)
