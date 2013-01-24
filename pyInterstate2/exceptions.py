class PyInterstateError(Exception):
    """Base class for Interstate App Exceptions."""
    generic_error_message = "Please see InterstateApp API documentation for more details."

class AuthError(PyInterstateError):
    """Exception raised upon authentication errors."""

class RequestError(PyInterstateError):
    """Exception raised upon violating standard request format."""
    pass

class RequestHasParamsError(RequestError):
    pass

class RequestRequiresParamsError(RequestError):
    pass

class IdError(PyInterstateError):
    """Raised when an operation attempts to query's an Interstate \
        Road or Roadmap that does not exist."""
    pass


