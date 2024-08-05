import logging
import re
from crlat_ob_client.odds_boost import OddsBoost
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

import requests
from lxml import html

from crlat_ob_client import OBException
from crlat_ob_client.login import OBLogin
from crlat_ob_client.utils.helpers import check_status_code, do_request
from datetime import datetime, timedelta

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    pass

from crlat_ob_client import LOGGER_NAME

_logger = logging.getLogger(LOGGER_NAME)


class Freeride(OddsBoost):
    customer = None

    def __init__(self, env, brand, redemption_value, freeride_name, *args, **kwargs):
        super(Freeride, self).__init__(env, brand, redemption_value, '', *args, **kwargs)
        self.redemption_value = redemption_value
        self.freeride_name = freeride_name