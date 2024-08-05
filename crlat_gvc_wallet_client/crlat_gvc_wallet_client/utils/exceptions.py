
class GVCUserClientException(BaseException):
    def __init__(self, message):
        super(GVCUserClientException, self).__init__(message)
