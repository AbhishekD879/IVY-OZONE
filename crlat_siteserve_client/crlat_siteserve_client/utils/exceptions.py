class SiteServeException(BaseException):
    def __init__(self, message):
        super(SiteServeException, self).__init__(message)
