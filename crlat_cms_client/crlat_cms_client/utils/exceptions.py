class CMSException(BaseException):
    def __init__(self, message):
        super(CMSException, self).__init__(message)
