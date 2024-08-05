from voltron.utils.exceptions.voltron_exception import VoltronException


class PreconditionNotMetException(VoltronException):
    """
        Common Exception to raise in case of not satisfying any preconditions
    """
