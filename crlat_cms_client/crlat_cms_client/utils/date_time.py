from datetime import datetime, timedelta
import pytz
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+
import logging
from crlat_cms_client import LOGGER_NAME

_logger = logging.getLogger(LOGGER_NAME)


def get_date_time_object(date_time_obj=None, tz_region='UTC', time_format="%Y-%m-%d", **kwargs):
    date_time = date_time_obj if date_time_obj else datetime.now(tz=pytz.timezone(tz_region))
    # _logger.debug('Current date is: %s, timedelta %s' % (date_time.strftime(time_format), kwargs))
    modified_date = date_time + timedelta(**kwargs)
    # _logger.debug('Modified date is: %s' % modified_date.strftime(time_format))
    return modified_date


def get_date_time_as_string(date_time_obj=None, tz_region='UTC', time_format="%Y-%m-%d", url_encode=False, **kwargs):
    modified_date = get_date_time_object(date_time_obj=date_time_obj, tz_region=tz_region, **kwargs)
    date_url = quote(modified_date.strftime(time_format)) if url_encode else modified_date.strftime(time_format)
    # _logger.debug('Modified date URL is: %s' % date_url)
    return date_url
