class PyInterstateError(Exception):
    """Base class for PyInterstate Exceptions."""
    generic_error_message = "Please see InterstateApp API documentation for more details."

class AuthError(PyInterstateError):
    """Exception raised upon authentication errors."""

class RequestError(PyInterstateError):
    """Base class for request specific Exceptions"""
    pass

class RequestHasParamsError(RequestError):
    """Exception raised when PUT or POST are not provided parameters"""
    pass

class RequestRequiresParamsError(RequestError):
    """Exception raised when PUT or POST are not provided parameters"""
    pass


