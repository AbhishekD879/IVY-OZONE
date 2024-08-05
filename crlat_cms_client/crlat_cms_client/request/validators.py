
import requests

from crlat_core.request.validators import RequestValidatorBase
from crlat_core.request.exceptions import RequestValidationException
from crlat_cms_client.utils.settings import get_cms_settings


class ProductionRequestValidator(RequestValidatorBase):

    _whitelist = ('/v1/api/login',)
    _allowed_methods = ('GET',)
    _restricted_backends = ('prd0',)

    def validate(self, request: requests.models.PreparedRequest, *_) -> None:
        """ Checks the validity of the request to production backends.
            If request type is other than GET and user is not trying to login,
            request should be denied and RequestValidationException is raised.

            :param request: request object
        """
        backend = get_cms_settings().backend
        self.logger.debug(
            f"Validate request to {request.path_url} on {backend} backend"
        )
        if (
            backend in self._restricted_backends
            and request.method.upper() not in self._allowed_methods
            and request.path_url not in self._whitelist
        ):
            raise RequestValidationException(
                f'Only {self._allowed_methods} requests are allowed for {backend} environment'
            )
