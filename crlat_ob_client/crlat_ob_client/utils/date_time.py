from datetime import datetime, timedelta

import logging
import re
from dateutil.parser import parse
import pytz

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+
from crlat_ob_client import LOGGER_NAME

_logger = logging.getLogger(LOGGER_NAME)


def get_date_time_object(date_time_obj=None, tz_region='GB', time_format="%Y-%m-%d", **kwargs):
    date_time = date_time_obj if date_time_obj else datetime.now(tz=pytz.timezone(tz_region))
    # _logger.debug('Current date is: %s, timedelta %s' % (date_time.strftime(time_format), kwargs))
    modified_date = date_time + timedelta(**kwargs)
    # _logger.debug('Modified date is: %s' % modified_date.strftime(time_format))
    return modified_date


def get_date_time_as_string(date_time_obj=None, tz_region='GB', time_format="%Y-%m-%d", url_encode=False, **kwargs):
    modified_date = get_date_time_object(date_time_obj=date_time_obj, tz_region=tz_region, **kwargs)
    date_url = quote(modified_date.strftime(time_format)) if url_encode else modified_date.strftime(time_format)
    # _logger.debug('Modified date URL is: %s' % date_url)
    return date_url


def strftime_add_day_suffix(datetime_string, format_pattern):
    suffixes = {'1': 'st', '2': 'nd', '3': 'rd', '21': 'st', '22': 'nd', '23': 'rd', '31': 'st'}
    datetime_obj = parse(datetime_string)
    x = datetime_obj.strftime(format_pattern)
    day_number = re.search(r'(\d{1,2})', x).group(0)
    suffix_to_add = suffixes.get(day_number, 'th')
    x = x.replace(day_number, '%s%s' % (day_number, suffix_to_add), 1)
    return x


def validate_time(actual_time, format_pattern='%H:%M %p'):
    try:
        datetime.strptime(actual_time, format_pattern)
        return True
    except ValueError as e:
        raise Exception('*** Actual time string: "%s" does not correspond to expected format: "%s" or error occured "%s"'
                               % (actual_time, format_pattern, e))
