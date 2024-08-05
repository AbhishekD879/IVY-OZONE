from native_ios.utils.exceptions.failure_exception import TestFailure


class SoftAssertException(TestFailure):
    """
    Common Exception to raise in case of soft asserts failures
    """
