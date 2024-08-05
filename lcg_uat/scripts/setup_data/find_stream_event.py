"""
Script is used for searching events with specific stream providers
Jira: VOL-4436
"""
# flake8: noqa
import argparse
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tests
from crlat_ob_client.utils.date_time import get_date_time_as_string
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter
from crlat_siteserve_client.utils.exceptions import SiteServeException
from tests import VoltronSettings
from tests import mobile_default
from tests.Common import Common
from voltron.utils.helpers import do_request


class FindStreamEvent(Common):
    device_name = mobile_default

    def find_events(self, args) -> dict:
        """
        Find event(s) with specific stream providers
        :param args: contains host_name, brand, backend env, events_number and stream provider
        :param host_name: str
        :param brand: str (optional parameter)
        :param backend_env: str (optional parameter)
        :param events_number: int
        :param stream_provider: str or list of stream provider codes
        :return: dict with event(s) url and stream provider or list with event(s) url
        Example:
        python scripts/setup_data/find_stream_event.py --host_name='sports-tst2.ladbrokes.com'
        --number_of_events=1 --stream_provider='EVFLAG_PVM,EVFLAG_IVM,EVFLAG_GVM'
        """
        origin_hostname = tests.HOSTNAME = args.host_name.replace('https://', '')
        settings = tests.settings = VoltronSettings(environment=origin_hostname, location='IDE')
        backend_env = settings.backend_env if args.host_name else args.backend_env
        brand = tests.settings.brand if args.host_name else args.brand
        category_id = str(args.category_id) if args.category_id else \
            '16,34,51,5,6,24,18,22,31,30,32,23,55,28,1,9,10,13,46,20,3,54,36,52,8,35,12,42'

        username = settings.betplacement_user
        self.site.login(username=username)

        self.__class__.start_date = f'{get_date_time_as_string(days=-1)}T22:00:00.000Z'
        self.__class__.end_date = f'{get_date_time_as_string(days=0)}T22:00:00.000Z'
        self.__class__.start_date_minus = get_date_time_as_string(time_format="%Y-%m-%dT%H:%M:%S")

        ss_req = SiteServeRequests(env=backend_env, brand=brand)
        stream_provider = args.stream_provider if isinstance(args.stream_provider, str) else ','.join(args.stream_provider)

        events_filter = self.basic_active_events_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, category_id)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.INTERSECTS, stream_provider)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.CONTAINS, 'EVFLAG_BL'))

        resp = ss_req.ss_event(event_id='', query_builder=events_filter)
        found_events = [event['event'] for event in resp if event.get('event')]

        if not found_events:
            raise SiteServeException(f'No active events found for stream flags "{stream_provider}"')

        event_urls = {}
        bpp_token = self.get_local_storage_cookie_value_as_dict('OX.USER')['bppToken']
        for event in found_events[:int(args.number_of_events)]:
            start_time_local = self.convert_time_to_local(
                date_time_str=event["startTime"], ob_format_pattern=self.ob_format_pattern)
            try:
                event_id = event["id"]
                headers = {'Accept': 'application/json, text/plain, */*',
                           'accept-encoding': 'gzip, deflate, br',
                           'accept-language': 'en-US,en;q=0.9',
                           'origin': f'https://{origin_hostname}',
                           'referer': f'https://{origin_hostname}/{event_id}',
                           'sec-fetch-mode': 'cors',
                           'sec-fetch-site': 'corss-site',
                           'token': bpp_token,
                           'user': username
                           }
                prov_code = do_request(url=f'{settings.optin_hostname}/api/video/igame/{event_id}',
                                       headers=headers, method='GET').get('priorityProviderCode')
            except Exception:
                continue
            else:
                event_url = f'https://{origin_hostname}/event/{event_id}'
                event_urls[event_url] = [start_time_local, prov_code] if prov_code else start_time_local

        if event_urls:
            ev = {k: v for k, v in sorted(event_urls.items(), key=lambda item: item[1])}
            self._logger.info(f'**** FOUND {len(ev)} EVENT(s) WITH ID(s): {ev}')
        else:
            self._logger.info(f'**** EVENTS WAS NOT FOUND FOR FLAGS: {args.stream_provider} AND CATEGORY ID {category_id}')

    @staticmethod
    def configure_arg_parser():
        # Get command line arguments
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("--host_name", "-host_name", help="HOSTNAME", default="sports-tst2.ladbrokes.com")
        arg_parser.add_argument("--brand", "-brand", help="Brand", default="ladbrokes", required=False)
        arg_parser.add_argument("--backend_env", "-backend_env", help="Backend env", default="tst2", required=False)
        arg_parser.add_argument("--number_of_events", "-number_of_events", help="Number of events", default=1, type=int)
        arg_parser.add_argument("--category_id", "-category_id", help="Category id", required=False)
        arg_parser.add_argument("--stream_provider", "-stream_provider", help="Stream provider",
                                default=['EVFLAG_PVM', 'EVFLAG_IVM', 'EVFLAG_GVM'])
        return arg_parser


if __name__ == "__main__":
    parser = FindStreamEvent.configure_arg_parser()
    args = parser.parse_args()
    a = FindStreamEvent()
    events = a.find_events(args)
