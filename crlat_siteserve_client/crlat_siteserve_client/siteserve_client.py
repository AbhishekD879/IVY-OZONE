import logging

from crlat_siteserve_client import LOGGER_NAME
from crlat_siteserve_client.query_params_builder import DebugFilterBuilder, ChildCountFilterBuilder, \
    ResponseFormatFilterBuilder
from crlat_siteserve_client.query_params_builder import ExistsFilterBuilder
from crlat_siteserve_client.query_params_builder import ExternalKeysBuilder
from crlat_siteserve_client.query_params_builder import LimitRecordsFilterBuilder
from crlat_siteserve_client.query_params_builder import PriceHistoryFilterBuilder
from crlat_siteserve_client.query_params_builder import PruneFilterBuilder
from crlat_siteserve_client.query_params_builder import QueryBuilder
from crlat_siteserve_client.query_params_builder import RacingFormFilterBuilder
from crlat_siteserve_client.query_params_builder import SimpleFilterBuilder
from crlat_siteserve_client.query_params_builder import TranslationLangFilterBuilder
from crlat_siteserve_client.utils.helpers import do_request
from crlat_siteserve_client.utils.helpers import extract_response

environments = {
    'ladbrokes': {
        'tst2': 'https://obbackoffice-tst2.internal.ladbrokes.com/',
        'stg2': 'https://obbackoffice-stg.internal.ladbrokes.com/',
        'prod': 'https://ss-aka-ori.ladbrokes.com/'
    },
    'bma': {
        'tst2': 'https://obbackoffice-tst2.internal.coral.co.uk/',
        'stg2': 'https://obbackoffice-stg.internal.coral.co.uk/',
        'prod': 'https://ss-aka-ori.coral.co.uk/'
    }
}
timeout = 30


class SiteServeRequests(object):
    @property
    def headers(self):
        return {'origin': self.site,
                'user-agent': 'Mozilla/5.0 (Linux; Android 9.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Mobile Safari/537.36',
                'accept': 'application/json, text/plain, */*',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'authority': self.site.replace('https://', ''),
                'accept-language': 'en-US,en;q=0.9'
                }

    def __init__(self, env, version='2.31', **kwargs):
        super(SiteServeRequests, self).__init__()
        self.brand = kwargs.get('brand', 'bma')
        self.class_id, self.category_id = kwargs.get('class_id'), kwargs.get('category_id')
        brand_env = environments[self.brand] if self.brand in environments else environments['bma']
        self.site = brand_env[env] if env in brand_env else brand_env['tst2']
        self.version = version
        self._logger = logging.getLogger(LOGGER_NAME)
        self.lotto_url = f'{self.site}openbet-ssviewer/Lottery/{self.version}/'
        self.base_url = f'{self.site}openbet-ssviewer/Drilldown/{self.version}/'
        self.historic_drilldown_url = f'{self.site}openbet-ssviewer/HistoricDrilldown/{self.version}/'

    def ss_coupon(self, coupon_id: str=None, query_builder: QueryBuilder=None, raise_exceptions: bool=True,
                  timeout:int=timeout) -> list:
        """
        Performs Coupon request to SiteServe
        :param coupon_id: coupon id
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return list of coupons
        """
        endpoint = f'Coupon/{coupon_id}' if coupon_id else 'Coupon'
        r = do_request(method='GET', url=f'{self.base_url}{endpoint}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_event_for_type(self, type_id: str = None, query_builder: QueryBuilder = None, raise_exceptions: bool = False,
                          timeout:int=timeout) -> list:
        """
        Performs Type request to SiteServe
        :param type_id: id of type
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list of events
        """
        r = do_request(method='GET', url=f'{self.base_url}EventForType/{type_id}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_class(self, class_id: str=None, query_builder: QueryBuilder=None, raise_exceptions: bool=False,
                 timeout:int=timeout) -> list:
        """
        Performs Class request to SiteServe
        :param class_id: id of class
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list of classes
        """
        endpoint = f'Class/{class_id}' if class_id else 'Class'
        r = do_request(method='GET', url=f'{self.base_url}{endpoint}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_event_to_outcome_for_event(self, event_id: (str, int), query_builder: QueryBuilder=None,
                                      raise_exceptions: bool=True, timeout:int=timeout) -> list:
        """
        Performs EventToOutcomeForEvent request to SiteServe
        :param event_id: id of event
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list of events
        """
        r = do_request(method='GET', url=f'{self.base_url}EventToOutcomeForEvent/{event_id}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_event_to_outcome_for_type(self, type_id, query_builder: QueryBuilder=None, raise_exceptions: bool=True,
                                     timeout:int=timeout):
        """
        Performs EventToOutcomeForType request to SiteServe
        :param type_id: type id
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list of events
        """
        r = do_request(method='GET', url=f'{self.base_url}EventToOutcomeForType/{type_id}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_event_to_outcome_for_class(self, class_id: (str, int)=None, query_builder: QueryBuilder=None,
                                      timeout:int=timeout) -> list:
        """
        Performs EventToOutcomeForClass request to SiteServe
        :param class_id: id or ids of classes
        :param query_builder: query parameters
        :param timeout: request timeout
        :return: list of events
        """
        classes_ids = None
        if isinstance(class_id, (str, int)):
            classes_ids = [class_id]
        elif isinstance(class_id, type(None)):
            classes_ids = self.class_id if isinstance(self.class_id, (list, tuple)) else [self.class_id]
        elif isinstance(class_id, (list, tuple)):
            classes_ids = class_id

        classes_dict = {}
        start, end = 0, 100
        while len(classes_ids) > start:
            slice_ = classes_ids[start:end]
            get_class_string = ','.join(map(str, slice_))
            r = do_request(method='GET', url=f'{self.base_url}EventToOutcomeForClass/{get_class_string}',
                           headers=self.headers,
                           params=query_builder.build() if query_builder else [],
                           timeout=timeout)
            try:
                classes_dict['SSResponse']['children'].extend(r['SSResponse']['children'])
            except KeyError:
                classes_dict.update(r)
            start += 100
            end += 100
        events_list = [x for x in classes_dict['SSResponse']['children'] if 'responseFooter' not in x.keys()]
        return events_list

    def ss_next_n_event_to_outcome_for_class(self,
                                             class_id: str=None, n: int=5,
                                             query_builder: QueryBuilder=None,
                                             raise_exceptions: bool=True,
                                             timeout:int=timeout) -> list:
        """
        Performs NextNEventToOutcomeForClass request to SiteServe
        :param class_id: id or ids of classes
        :param n: number of events
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list of events
        """
        class_id = class_id if class_id else self.class_id
        r = do_request(method='GET', url=f'{self.base_url}NextNEventToOutcomeForClass/{n}/{class_id}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)

        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_event_to_market_for_class(self, class_id: str=None, query_builder: QueryBuilder=None,
                                             raise_exceptions: bool=True, timeout:int=timeout) -> list:
        """
        Performs EventToMarketForClass request to SiteServe
        :param class_id: id of class
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list of events
        """
        class_id = class_id if class_id else self.class_id
        r = do_request(method='GET', url=f'{self.base_url}EventToMarketForClass/{class_id}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)

        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_events_to_outcome_for_markets(self, market_ids: list,
                                         query_builder: QueryBuilder=None,
                                         raise_exceptions: bool=False,
                                         timeout:int=timeout) -> list:
        """
        Performs EventToOutcomeForMarket request to SiteServe
        :param market_ids: id or ids of classes
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list of events
        """
        take_elements = market_ids
        while len(take_elements) > 0:
            slice = take_elements[:100]
            del take_elements[:100]
            get_markets_string = ','.join(map(str, slice))
            r = do_request(method='GET', url=f'{self.base_url}EventToOutcomeForMarket/{get_markets_string}',
                           headers=self.headers,
                           params=query_builder.build() if query_builder else [],
                           timeout=timeout)
            return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_coupon_to_outcome_for_coupon(self, coupon_id: (int, str), query_builder: QueryBuilder=None,
                                        raise_exceptions: bool=False, timeout:int=timeout) -> list:
        """
        Performs CouponToOutcomeForCoupon request to SiteServe
        ::param coupon_id: numeric or string id of specific coupon
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list of events dictionaries
        """
        r = do_request(method='GET', url=f'{self.base_url}CouponToOutcomeForCoupon/{coupon_id}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_event(self, event_id: (int, str), query_builder: QueryBuilder=None, raise_exceptions: bool=False,
                 timeout:int=timeout):
        """
        Performs Event request to SiteServe
        :param event_id: numeric or string id of specific coupon
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list of events dictionaries
        """
        r = do_request(method='GET', url=f'{self.base_url}Event/{event_id}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_pool(self, pool_id: (int, str)=None, query_builder: QueryBuilder=None, raise_exceptions: bool=True,
                timeout:int=timeout) -> list:
        """
        Performs Pool request to SiteServe
        :param pool_id: numeric or string id of specific pool
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list of events dictionaries
        """
        endpoint = f'Pool/{pool_id}' if pool_id else 'Pool'
        r = do_request(method='GET', url=f'{self.base_url}{endpoint}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_pool_for_class(self, class_id: (int, str)=None, query_builder: QueryBuilder=None, raise_exceptions: bool=True,
                          timeout:int=timeout) -> list:
        """
        Performs PoolForClass request to SiteServe
        :param class_id: numeric or string id of specific class
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list of events dictionaries
        """
        class_id = class_id if class_id else self.class_id
        r = do_request(method='GET', url=f'{self.base_url}PoolForClass/{class_id}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_lottery_to_draw(self, query_builder: QueryBuilder = None, raise_exceptions: bool = True,
                           timeout:int=timeout) -> list:
        """
        Performs LotteryToDraw request to SiteServe
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list with dictionaries
        """
        r = do_request(method='GET', url=f'{self.lotto_url}LotteryToDraw',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_pool_for_event(self, event_id: (int, str), query_builder: QueryBuilder=None,
                          raise_exceptions: bool=False, timeout:int=timeout) -> list:
        """
        Performs PoolForEvent request to SiteServe
        :param event_id: id of specific event
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list with dictionaries
        """
        r = do_request(method='GET', url=f'{self.base_url}PoolForEvent/{event_id}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_pool_to_pool_value(self, pool_id: (int, str), query_builder: QueryBuilder=None, raise_exceptions: bool=True,
                              timeout:int=timeout) -> list:
        """
        Performs PoolToPoolValue request to SiteServe
        :param pool_id: id of specific pool
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list with dictionaries
        """
        r = do_request(method='GET', url=f'{self.base_url}PoolToPoolValue/{pool_id}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_resulted_event(self, event_id: (str, int), query_builder: QueryBuilder=None, raise_exceptions: bool=True,
                          timeout:int=timeout) -> list:
        """
        Performs ResultedEvent request to SiteServe
        :param event_id: id of specific resulted event
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list with dictionaries
        """
        r = do_request(method='GET', url=f'{self.historic_drilldown_url}ResultedEvent/{event_id}',
                       headers=self.headers,
                       params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_class_to_sub_type_for_type(self, type_ids: (str, list),
                                      query_builder: QueryBuilder=None,
                                      raise_exceptions: bool=True,
                                      timeout:int=timeout) -> list:
        """
        Performs ClassToSubTypeForType request to SiteServe
        :param type_ids: type id or list of ids
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list with dictionaries
        """
        if isinstance(type_ids, list):
            type_ids = ",".join(type_ids)
        r = do_request(method='GET', url=f'{self.base_url}ClassToSubTypeForType/{type_ids}',
                       headers=self.headers, params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_class_to_sub_type_for_class(self, class_id: (str, int), query_builder: QueryBuilder=None,
                                       raise_exceptions: bool=True, timeout:int=timeout):
        """
        Performs ClassToSubTypeForClass to SiteServe
        :param class_id: numeric or string id of specific class
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list with dictionaries
        """
        r = do_request(method='GET', url=f'{self.base_url}ClassToSubTypeForClass/{class_id}',
                       headers=self.headers, params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)

    def ss_class_to_template_market_for_type(self, type_id: (str, int), query_builder: QueryBuilder=None,
                                             raise_exceptions: bool=True, timeout:int=timeout):
        """
        Performs ClassToTemplateMarketForType to SiteServe
        :param type_id: numeric or string id of specific type
        :param query_builder: query parameters
        :param raise_exceptions: whether to raise exception on empty response or not
        :param timeout: request timeout
        :return: list with dictionaries
        """
        r = do_request(method='GET', url=f'{self.base_url}ClassToTemplateMarketForType/{type_id}',
                       headers=self.headers, params=query_builder.build() if query_builder else [],
                       timeout=timeout)
        return extract_response(response=r, raise_exceptions=raise_exceptions)


query_builder = QueryBuilder
simple_filter = SimpleFilterBuilder
exists_filter = ExistsFilterBuilder
external_keys = ExternalKeysBuilder
translation_lang = TranslationLangFilterBuilder
racing_form = RacingFormFilterBuilder
prune = PruneFilterBuilder
price_history = PriceHistoryFilterBuilder
limit_records = LimitRecordsFilterBuilder
debug_filter = DebugFilterBuilder
child_count_filter = ChildCountFilterBuilder
response_format_filter = ResponseFormatFilterBuilder
