from native_ios.utils.exceptions.voltron_exception import VoltronException


class SiteServeException(VoltronException):
    """
    SiteServeException to raise in case of missing required SS data
    """

    @staticmethod
    def _attach_screenshot():
        """
        Bypassed adding screenshot as Exception is raised not on UI exceptions
        """
        pass
