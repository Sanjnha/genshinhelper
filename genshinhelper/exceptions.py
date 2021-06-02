from .utils import log


class GenshinHelperException(Exception):
    """Base genshinhelper exception."""

    def __init__(self, message):
        super().__init__(message)
        log.error(message)


class CookiesExpired(GenshinHelperException):
    """Cookies has expired."""


class NotificationError(GenshinHelperException):
    """
    A notification error. Raised after an issue with the sent notification.
    """


class NoSuchNotifierError(GenshinHelperException):
    """
    An unknown notifier was requests, one that was not registered.
    """
