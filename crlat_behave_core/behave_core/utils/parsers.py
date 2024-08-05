import ujson as json
from datetime import datetime, timedelta
from string import Template

import pytz

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+


def proceed_json_with_variables(json_body, parameters):
    with open(json_body, 'r', encoding="utf-8") as file:
        read_data = file.read()
    formatted_data = Template(read_data).safe_substitute(parameters)
    formatted_data = Template(formatted_data).safe_substitute(substitute_time())
    return json.loads(formatted_data)


def substitute_time():
    curr_time = datetime.now()
    time_format = '%Y-%m-%dT%H:%M:%S.%f'
    prev = (curr_time - timedelta(days=1)).strftime('%Y-%m-%d')
    curr = (curr_time + timedelta(days=1)).strftime('%Y-%m-%d')
    prev_date = (curr_time - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    curr_date = (curr_time + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    event_current = curr_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    event_future = (curr_time + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    expired_past = (curr_time - timedelta(days=30)).strftime('%Y-%m-%d')
    expired_curr = (curr_time - timedelta(days=29)).strftime('%Y-%m-%d')
    expired_time_zone_prev = get_date_time_as_string(date_time_obj=curr_time, time_format=time_format, url_encode=False,
                                                     days=-10)[:-3] + 'Z'
    expired_time_zone_curr = get_date_time_as_string(date_time_obj=curr_time, time_format=time_format, url_encode=False,
                                                     days=-5)[:-3] + 'Z'
    inactive_time_zone_prev = get_date_time_as_string(date_time_obj=curr_time, time_format=time_format,
                                                      url_encode=False, days=-4)[:-3] + 'Z'
    inactive_time_zone_curr = get_date_time_as_string(date_time_obj=curr_time, time_format=time_format,
                                                      url_encode=False, days=-1)[:-3] + 'Z'
    time_zone_prev = get_date_time_as_string(date_time_obj=curr_time, time_format=time_format, url_encode=False,
                                             days=-1)[:-3] + 'Z'
    time_zone_curr = get_date_time_as_string(date_time_obj=curr_time, time_format=time_format, url_encode=False,
                                             days=+1)[:-3] + 'Z'
    time_zone_prev_end_in_min = get_date_time_as_string(date_time_obj=curr_time, time_format=time_format,
                                                        url_encode=False,
                                                        hours=-3,  # due to UTC time zone
                                                        minutes=+1
                                                        )[:-3] + 'Z'
    future_time_zone_prev = get_date_time_as_string(date_time_obj=curr_time, time_format=time_format, url_encode=False,
                                                    days=+1)[:-3] + 'Z'
    future_time_zone_prev_start_in_min = get_date_time_as_string(date_time_obj=curr_time, time_format=time_format,
                                                                 url_encode=False, hours=-3,  # due to UTC time zone
                                                                 minutes=+1)[:-3] + 'Z'
    future_time_zone_curr = get_date_time_as_string(date_time_obj=curr_time, time_format=time_format, url_encode=False,
                                                    days=+3)[:-3] + 'Z'
    return {
        'past': prev,
        'curr': curr,
        'prev_date': prev_date,
        'curr_date' : curr_date,
        'expired_past': expired_past,
        'expired_curr': expired_curr,
        'expired_time_zone_prev': expired_time_zone_prev,
        'expired_time_zone_curr': expired_time_zone_curr,
        'inactive_time_zone_prev': inactive_time_zone_prev,
        'inactive_time_zone_curr': inactive_time_zone_curr,
        'time_zone_prev': time_zone_prev,
        'time_zone_curr': time_zone_curr,
        'time_zone_prev_end_in_min': time_zone_prev_end_in_min,
        'future_time_zone_prev': future_time_zone_prev,
        'future_time_zone_prev_start_in_min': future_time_zone_prev_start_in_min,
        'future_time_zone_curr': future_time_zone_curr,
        'event_current': event_current,
        'event_future': event_future
    }


def get_date_time_object(date_time_obj=None, tz_region='UTC', time_format="%Y-%m-%d", **kwargs):
    date_time = date_time_obj if date_time_obj else datetime.now(tz=pytz.timezone(tz_region))
    modified_date = date_time + timedelta(**kwargs)
    return modified_date


def get_date_time_as_string(date_time_obj=None, tz_region='UTC', time_format="%Y-%m-%d", url_encode=False, **kwargs):
    modified_date = get_date_time_object(date_time_obj=date_time_obj, tz_region=tz_region, **kwargs)
    date_url = quote(modified_date.strftime(time_format)) if url_encode else modified_date.strftime(time_format)
    return date_url
