from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException


class GVCException(ThirdPartyDataException):
    """
    Common Exception to raise in case of missing GVC side configuration
    """
