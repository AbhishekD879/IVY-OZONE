from voltron.utils.exceptions.voltron_exception import VoltronException


class CmsClientException(VoltronException):
    """
    CmsClientException for raise in case of incorrect/unexpected CMS configuration
    """

    @staticmethod
    def _attach_screenshot():
        """
        Bypassed adding screenshot as Exception is raised not on UI exceptions
        """
        pass
