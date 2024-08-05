class TestRailAPIError(BaseException):
    def __init__(self, message):
        super(TestRailAPIError, self).__init__(message)
