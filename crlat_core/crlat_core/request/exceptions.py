from crlat_core.exceptions import CRLATException


class RequestValidationException(CRLATException):
    def __init__(self, message):
        super(RequestValidationException, self).__init__(message)


class InvalidResponseException(CRLATException):
    def __init__(self, message):
        super(InvalidResponseException, self).__init__(message)
