from voltron.utils.exceptions.siteserve_exception import SiteServeException


class ThirdPartyDataException(SiteServeException):
    """
    Common Exception to raise in case of missing 3rd party data
    e.g. TimeForm, DataFabric, Racing Post, etc..
    """
