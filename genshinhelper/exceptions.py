class GenshinHelperException(Exception):
    """Base genshinhelper exception."""


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
