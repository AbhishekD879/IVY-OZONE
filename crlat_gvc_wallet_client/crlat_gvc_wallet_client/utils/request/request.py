import logging

import urllib3
from crlat_core.request import Request

from crlat_gvc_wallet_client import LOGGER_NAME
from crlat_gvc_wallet_client.utils.settings import get_gvc_settings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GVCUserClientRequest(Request):

    def __init__(self, **kwargs):
        gvc_settings = get_gvc_settings()

        parser = kwargs.pop('parser', None)
        use_session = kwargs.pop('use_session', True)
        headers = {'accept': 'application/json',
                   'Content-Type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (Linux; Android 9.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Mobile Safari/537.36 Frontend-Automation',
                   'Origin': gvc_settings.config.base_host_url}
        headers.update(kwargs.pop('headers', {}))

        hostname = kwargs.pop('hostname', gvc_settings.config.mobileportal)

        super(GVCUserClientRequest, self).__init__(
            use_session=use_session,
            headers=headers,
            parser=parser,
            validators=[],
            hostname=hostname,
            **kwargs
        )

    logger = logging.getLogger(LOGGER_NAME).getChild('[request]')
