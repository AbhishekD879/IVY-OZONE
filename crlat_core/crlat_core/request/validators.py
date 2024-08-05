import abc
import logging

import requests


class RequestValidatorBase(metaclass=abc.ABCMeta):
    """ Base class for request validator. Just before a request is made a validate
        method is called with `requests.PreparedRequest` and `requests.Session provided`.
        validate validate function can then throw `RequestValidationException` if
        request and/or session is nod valid
    """

    logger = logging.getLogger('crlat_cms_client')

    @abc.abstractmethod
    def validate(self, request: requests.models.PreparedRequest, session: requests.sessions.Session) -> None:
        """ Checks the validity of the request based on request and session object

            :param request: request object
            :param session: session object
        """
        pass
