from voltron.utils.exceptions.voltron_exception import VoltronException


class DeviceException(VoltronException):
    """
    Currently used in cases where is needed to get device information from xcode-cli
    """

    @staticmethod
    def _attach_screenshot():
        """
        Bypassed adding screenshot as Exception is raised not on UI exceptions
        """
        pass
