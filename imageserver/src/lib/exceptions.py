class OwnzonesException(Exception):
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return repr(self.value)

class BaseImageNotFound(OwnzonesException):
    pass

class ImageNotInCache(OwnzonesException):
    pass

class NotAnImageFile(OwnzonesException):
    pass

class NotAnImagePath(OwnzonesException):
    pass

class InvalidImageSize(OwnzonesException):
    pass
