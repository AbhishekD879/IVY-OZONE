from native_ios.utils.exceptions.voltron_exception import VoltronException


class TestFailure(VoltronException):
    """
    TestFailure for unittests checks (assertEqual, assertTrue, etc.)
    """
