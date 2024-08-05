import random
import re
from collections import namedtuple
from collections import OrderedDict
from datetime import datetime
from datetime import timedelta

from crlat_cms_client.request import CMSAPIRequest
from crlat_ob_client.tote_config import ToteOBConfig
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import query_builder
from crlat_siteserve_client.siteserve_client import racing_form
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from crlat_siteserve_client.siteserve_client import translation_lang
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
from dateutil.parser import parse
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import TryAgain

import tests
import voltron.environments.constants as vec
from tests.Common import Common
from voltron.utils.bpp_config import BPPConfig
from voltron.utils.datafabric.datafabric import Datafabric
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.general_exception import GeneralException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_modules_from_ws, get_response_url, do_request
from voltron.utils.helpers import get_racing_module_from_ws
from voltron.utils.timeform_client.timeform_client import TimeformClient
from voltron.utils.waiters import wait_for_result


class BaseRacing(Common):
    _ss_config = None
    event_name_on_landing_page = None
    expected_favourite_icons = {'lowest': 'F', 'second_lowest': '2F', 'lowest_pair': 'JF', 'second_lowest_pair': '2JF'}
    ew_terms = {'ew_places': 2, 'ew_fac_num': 1, 'ew_fac_den': 16}
    yc_specials_type_name = vec.racing.YOURCALL_SPECIALS.upper()
    expected_numbers_of_next_races_event = '12'
    _enhanced_races_name = ''
    _next_races_name = ''
    start_date = f'{get_date_time_as_string(days=0, hours=1, time_format="%Y-%m-%dT%H:%M:%S.000Z")}'

    @classmethod
    def get_ss_config(cls):
        if not cls._ss_config:
            ob_config = cls.get_ob_config()
            cls._ss_config = SiteServeRequests(env=tests.settings.backend_env,
                                               brand=cls.brand,
                                               category_id=ob_config.backend.ti.horse_racing.category_id,
                                               class_id=ob_config.backend.ti.horse_racing.class_ids
                                               )
        return cls._ss_config

    @classmethod
    def custom_setUp(cls, **kwargs):
        cls.get_ss_config()

    @classmethod
    def setup_cms_next_races_number_of_events(cls):
        next_races = cls.get_initial_data_system_configuration().get('NextRaces', {})
        if not next_races:
            next_races = cls.get_cms_config().get_system_configuration_item('NextRaces')
        number = next_races.get('numberOfEvents')
        if not number:
            raise CmsClientException('Number of events is not configured for Next Races section in CMS')
        if str(number) != str(cls.expected_numbers_of_next_races_event):
            cls.get_cms_config().set_next_races_numbers_of_event(number_of_event=cls.expected_numbers_of_next_races_event)

    def check_and_setup_cms_next_races_for_type(self, type_id: (list, str, int)):
        """
        Method to check if events from specific type will be shown on NextRaces module
        :param type_id: type id from SS (or list of types)
        :return:
        """
        next_races_config = self.get_initial_data_system_configuration().get('NextRaces', {})
        if not next_races_config:
            next_races_config = self.cms_config.get_system_configuration_item('NextRaces')
        next_races_type_id = next_races_config.get('typeID', '')
        if not next_races_type_id:
            self._logger.debug('No specific type id configured so all types will be shown')
        else:
            if isinstance(type_id, (str, int)):
                type_id = [type_id]
            type_id_need_to_be_updated = False
            for type_id_ in type_id:
                if str(type_id_) not in next_races_type_id:
                    type_id_need_to_be_updated = True
                    next_races_type_id = f'{next_races_type_id},{type_id_}'
            if type_id_need_to_be_updated:
                self.cms_config.update_system_configuration_structure(config_item='NextRaces',
                                                                      field_name='typeID',
                                                                      field_value=next_races_type_id)

    @property
    def end_date(self):
        """
        Preserving default end date filter for Racing - today events
        :return: end date string
        """
        days = 1
        end_date = f'{get_date_time_as_string(days=days)}T00:00:00.000Z'
        return end_date

    @property
    def category_id(self):
        return self.ob_config.backend.ti.horse_racing.category_id

    def get_order_of_modules(self):
        ordered_list_of_modules = []
        modules = get_modules_from_ws(category_id=self.category_id)
        for module in modules:
            if module.get('@type', '') == 'RacingModule':
                if self.brand == 'bma' and self.device_type == 'desktop':
                    module_name = ' '.join([w.title() if w.islower() else w for w in module.get('title', '').split()])
                else:
                    module_name = module.get('title', '').upper()
                ordered_list_of_modules.append(module_name)
        if not ordered_list_of_modules:
            ordered_list_of_modules = [vec.racing.UK_AND_IRE_TYPE_NAME, vec.racing.INTERNATIONAL_TYPE_NAME, vec.racing.LEGENDS_TYPE_NAME]
        return ordered_list_of_modules

    @property
    def type_flag_codes(self):
        return {'UK,IE': self.uk_and_ire_type_name,
                'FR': vec.racing.FRANCE_TYPE_NAME,
                'IN': vec.racing.INDIA_TYPE_NAME,
                'AE': vec.racing.UAE_TYPE_NAME,
                'CL': vec.racing.CHILE_TYPE_NAME,
                'AU': vec.racing.AUSTRALIA_TYPE_NAME,
                'US': vec.racing.USA_TYPE_NAME,
                'ZA': vec.racing.SOUTH_AFRICA_TYPE_NAME,
                'INT': self.international_type_name,
                'VR': self.legends_type_name}

    def get_type_name_from_flag_codes(self, event_flag_codes):
        known_flag_codes = []
        for flag in self.type_flag_codes.keys():
            if ',' not in flag:
                known_flag_codes.append(flag)
            else:
                known_flag_codes += flag.split(',')

        for flag_code in event_flag_codes:
            if flag_code in known_flag_codes:
                if flag_code in 'UK,IE':
                    flag_code = 'UK,IE'
                return self.type_flag_codes.get(flag_code)

    @property
    def uk_and_ire_type_name(self):
        request = CMSAPIRequest()
        env = tests.settings.cms_env
        if env == 'hlv0':
            env = 'hl'
        elif env == 'prd0':
            env = 'prod'
        url = f'https://cms-{env}.coral.co.uk/cms/api/bma/fsc/21' if self.brand == 'bma' else \
            f'https://cms-{env}.ladbrokes.com/cms/api/ladbrokes/fsc/21'
        response = request.get(url=url)
        name = next((module.get('title') for module in response['modules'] if module.get('racingType') == 'UIR'),None)
        if not name:
            raise CmsClientException('UK AND IRISH RACES racing type is not found CMS FSC 21 Call')
        return name

    @property
    def international_type_name(self):
        name = get_racing_module_from_ws(category_id=self.category_id, name='IR').get('title', vec.racing.INTERNATIONAL_TYPE_NAME)
        if self.brand == 'bma' and self.device_type == 'desktop':
            name = name
        else:
            name = name.upper()
        return name

    @property
    def virtual_type_name(self):
        # shown as "VIRTUAL RACE" (uppercased) in all cases
        return get_racing_module_from_ws(category_id=self.category_id, name='VRC').get('title', vec.racing.VIRTUAL_TYPE_NAME).upper()

    @property
    def legends_type_name(self):
        name = get_racing_module_from_ws(category_id=self.category_id, name='LVR').get('title', vec.racing.LEGENDS_TYPE_NAME)
        if self.brand == 'bma' and self.device_type == 'desktop':
            name = name
        else:
            name = name.upper()
        return name

    @property
    def international_tote_type_name(self):
        # shown as "INTERNATIONAL TOTE CAROUSEL" (uppercased) in all cases
        return get_racing_module_from_ws(category_id=self.category_id, name='ITC').get('title', vec.racing.INTERNATIONAL_TOTE_NAME).upper()

    @property
    def default_market_name(self):
        return self.ob_config.backend.ti.horse_racing.default_market_name.strip('|')

    @property
    def horseracing_autotest_uk_name_pattern(self):
        return self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern

    @property
    def horseracing_autotest_vr_name_pattern(self):
        return self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_virtual.name_pattern

    @property
    def horseracing_autotest_winning_distances_name_pattern(self):
        return self.ob_config.backend.ti.horse_racing.daily_racing_specials.winning_distances.name_pattern

    @property
    def horseracing_autotest_int_name_pattern(self):
        return self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_international.name_pattern

    @property
    def horseracing_autotest_ie_name_pattern(self):
        return self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_ireland.name_pattern

    @property
    def greyhound_autotest_name_pattern(self):
        return self.ob_config.backend.ti.greyhound_racing.greyhounds_live.autotest.name_pattern

    @property
    def horseracing_autotest_enhanced_multiples_name_pattern(self):
        return self.ob_config.backend.ti.horse_racing.daily_racing_specials.enhanced_multiples.name_pattern.upper()

    @property
    def horseracing_autotest_specials_name_pattern(self):
        return self.ob_config.backend.ti.horse_racing.horse_racing_specials.racing_specials.name_pattern.upper()

    @property
    def horse_racing_live_class_ids(self):
        class_ids = self.ob_config.backend.ti.horse_racing.class_ids
        class_ids.replace('%s,' % self.ob_config.backend.ti.horse_racing.daily_racing_specials.class_id, '')
        return class_ids

    @staticmethod
    def get_time_format_pattern_for_desktop(event_time: str = None, day: int = None):
        """
        :param event_time: event time in string OB format e.g. '2020-03-21T00:00:00.000Z'
        :param day: day of event in int format
        :return: format pattern with correct suffix
        """
        if event_time:
            event_day = parse(event_time, yearfirst=True).day
        if day:
            event_day = day

        if 4 <= event_day <= 20 or 24 <= event_day <= 30:
            suffix = 'th'
        else:
            suffix = ['st', 'nd', 'rd'][event_day % 10 - 1]
        format_pattern = f'%A %d{suffix} %B'
        return format_pattern

    def get_expected_day_tab_names(self, start_date):
        query_params_today = self.basic_query_params \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, datetime.now() + timedelta(days=6))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, start_date))

        resp = self.ss_req_hr.ss_event_to_outcome_for_class(query_builder=query_params_today)
        start_time = [start_time['event']['startTime'].rsplit('T')[0] for start_time in resp]
        unique_events_time = sorted(set(start_time))
        pattern = '%A' if self.brand == 'ladbrokes' or len(unique_events_time) < 4 else '%a'
        if self.brand != 'ladbrokes':
            expected_tabs = [parse(event_time).strftime(pattern).upper() for event_time in unique_events_time]
        else:
            expected_tabs = [parse(event_time).strftime(pattern) for event_time in unique_events_time]
        return expected_tabs

    def calculate_each_way_coef(self, each_way_market):
        """
        Verify and calculate E/W Coef for Horse Racing E/W market
        :param each_way_market: Horse Racing E/W market
        :return: Calculated coef
        """
        num = each_way_market.get('eachWayFactorNum', '')
        den = each_way_market.get('eachWayFactorDen', '')
        self.assertTrue(num.isdigit(), msg=f'"eachWayFactorNum" value "{num}" is not digit')
        self.assertTrue(den.isdigit(), msg=f'"eachWayFactorDen" value "{den}" is not digit')
        return int(num) / int(den)

    def is_event_present(self, event_name, group_name, is_present=True, timeout=0):
        self._logger.info('*** Event name: %s' % event_name)

        def _is_event_present(self):
            groups = self.site.horse_racing.tab_content.accordions_list.items
            if group_name in groups:
                groups[group_name].expand()
                self.assertTrue(groups[group_name].items_as_ordered_dict,
                                msg='No events was found in group "%s"' % group_name)
                return event_name in groups[group_name].items_as_ordered_dict
            else:
                return False

        result = wait_for_result(lambda: _is_event_present(self),
                                 expected_result=is_present,
                                 timeout=timeout,
                                 bypass_exceptions=(NoSuchElementException,
                                                    StaleElementReferenceException,
                                                    KeyError),
                                 name='Event "{0}" displaying state mach "{1}" in section "{2}"'.format(
                                     event_name, is_present, group_name))
        return result

    @property
    def enhanced_races_name(self) -> str:
        if not self._enhanced_races_name:
            featured_races_cms_config = self.get_initial_data_system_configuration().get('featuredRaces')
            if not featured_races_cms_config:
                featured_races_cms_config = self.cms_config.get_system_configuration_item('featuredRaces')
            self.__class__._enhanced_races_name = featured_races_cms_config.get('title').upper()
        return self._enhanced_races_name

    @property
    def next_races_title(self) -> str:
        if not self._next_races_name:
            next_races_config = self.get_initial_data_system_configuration().get('NextRaces')
            if not next_races_config:
                next_races_config = self.cms_config.get_system_configuration_item('NextRaces')
            next_races_title = next_races_config.get('title').strip()
            is_mobile = True if self.device_type in ['mobile', 'tablet'] else False
            if self.brand == 'ladbrokes':
                self.__class__._next_races_name = next_races_title.upper()
            else:
                self.__class__._next_races_name = next_races_title.upper() if is_mobile else next_races_title.title()
        return self._next_races_name

    def get_next_races_selections_number_from_cms(self) -> int:
        next_races_config = self.get_initial_data_system_configuration().get('NextRaces')
        if not next_races_config:
            next_races_config = self.cms_config.get_system_configuration_item('NextRaces')
        number = next_races_config.get('numberOfSelections')
        return int(number)

    def get_greyhound_next_races_selections_number_from_cms(self) -> int:
        next_races_config = self.get_initial_data_system_configuration().get('GreyhoundNextRaces')
        if not next_races_config:
            next_races_config = self.cms_config.get_system_configuration_item('GreyhoundNextRaces')
        number = next_races_config.get('numberOfSelections')
        return int(number)

    def get_sections(self, page_name):
        if page_name == 'horse-racing':
            contents = self.site.horse_racing
        elif page_name == 'greyhound-racing':
            contents = self.site.greyhound
        else:
            contents = self.site.horse_racing
        sections = contents.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found on page')
        return sections

    @retry(stop=stop_after_attempt(2), retry=retry_if_exception_type(StaleElementReferenceException), reraise=True)
    def get_racing_event(self, section_name=None, date_time=None, meeting_name=None, event_off_time=None, page_name=None):
        not_resulted_event = None
        meeting_name = meeting_name if self.brand == 'ladbrokes' else meeting_name.upper()
        sections = self.get_sections(page_name)
        if section_name and meeting_name and event_off_time:
            section = sections.get(section_name)
            self.assertTrue(section, msg=f'Section "{section_name}" was not found in "{sections.keys()}"')
            if date_time:
                days = section.date_tab.items_as_ordered_dict
                pattern = '%A' if len(days) < 4 else '%a'
                day_name = parse(date_time).strftime(pattern).upper()
                day = days.get(day_name)
                self.assertTrue(day_name, msg='"%s" is not found among "%s"' % (day_name, days.keys()))
                day.click()
                sections = self.get_sections(page_name)  # because sections got refreshed after clicking on date tab
                section = sections.get(section_name)
                self.assertTrue(section, msg='Section "%s" was not found' % section_name)
            section.expand()
            meetings = section.items_as_ordered_dict
            self.assertTrue(meetings, msg='No one meeting was found in section: "%s"' % section_name)
            meeting = meetings.get(meeting_name)
            self.assertTrue(meeting, msg=f'"{meeting_name}" meeting was not found in "{meetings.keys()}"')
            meeting.scroll_to()

            events = meeting.items_as_ordered_dict
            self.assertTrue(events, msg='No one event was found in row: "%s"' % meeting_name)
            self.__class__.event = events.get(event_off_time)
            self.assertTrue(self.event, msg=f'Event with off time "{self.event_off_time}" was not found among "{list(events.keys())}"')
            not_resulted_event = self.event
        else:
            skip_list = [self.next_races_title,
                         vec.racing.YOURCALL_SPECIALS.upper(),
                         self.enhanced_races_name,
                         vec.racing.ENHANCED_MULTIPLES_NAME]
            for section_name, section in sections.items():
                if section_name not in skip_list:
                    break
            meetings = section.items_as_ordered_dict
            self.assertTrue(meetings, msg='No one meeting was found in section: "%s"' % section_name)
            for meeting_name, meeting in meetings.items():
                meeting.scroll_to()
                events = meeting.items_as_ordered_dict
                self.assertTrue(events, msg='No one event was found in row: "%s"' % meeting_name)
                for event_name, event in events.items():
                    has_icon = event.is_resulted
                    self._logger.info('***** Event is: "%s". Its resulted status is: "%s"' % (event_name, has_icon))
                    if has_icon:
                        continue
                    self.__class__.event = not_resulted_event = event
                    break

        if not not_resulted_event:
            raise GeneralException('Can\'t find not resulted event')
        self.__class__.event_name_on_landing_page = '%s %s' % (not_resulted_event.name, meeting_name)
        self._logger.info('*** Selected event: %s ' % self.event_name_on_landing_page)
        return not_resulted_event

    def open_racing_event_details(self, section_name=None, date_time=None, meeting_name=None, event_off_time=None, page_name='horse-racing'):
        event = self.get_racing_event(section_name=section_name, date_time=date_time,
                                      meeting_name=meeting_name, event_off_time=event_off_time, page_name=page_name)
        event.click()
        timeout = tests.settings.edp_timeout
        if page_name == 'horse-racing':
            self.site.wait_content_state(state_name='RacingEventDetails', timeout=timeout)
        elif page_name == 'greyhound-racing':
            self.site.wait_content_state(state_name='GreyHoundEventDetails', timeout=timeout)

    def add_selection_to_quick_bet(self, outcome_name=None):
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % section_name)
        if outcome_name:
            self.assertIn(outcome_name, outcomes.keys(),
                          msg=f'Outcome "{outcome_name}" is not in list of created outcomes "{outcomes.keys()}"')
        outcome = outcomes[outcome_name] if outcome_name else list(outcomes.values())[0]
        outcome.bet_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=15), msg='Quick Bet is not shown')

    def verify_extra_place_icon_displayed(self, bet_leg, expected: bool = True):
        """
        Verifies if 'Extra place icon' is displayed (correctly) for given bet leg.
        :param bet_leg: specifies bet-leg
        :param expected: specifies if 'Extra Place' is expected to be displayed
        """
        if expected:
            self.assertTrue(bet_leg.has_promo_icon(), msg='Failed to display "Extra Place" icon')
            self.assertEquals(bet_leg.promo_label_text, vec.racing.EXTRA_PLACE,
                              msg='Incorrect "Extra Place" label text.\nActual: "%s"\nExpected: "%s"'
                                  % (bet_leg.promo_label_text, vec.racing.EXTRA_PLACE))
        else:
            self.assertFalse(bet_leg.has_promo_icon(expected_result=False),
                             msg='"Extra Place" icon is displayed which is unexpected')

    _next_races = None

    def get_next_races_section(self):
        if self._next_races:
            try:
                self._next_races.is_displayed(timeout=0.5)
            except StaleElementReferenceException as e:
                self._logger.debug(f'*** Next Races content refreshed: "{e}"')
                self.__class__._next_races = None

        if not self._next_races:
            page = self.site.horse_racing if self.site.wait_content_state('Horseracing', timeout=1,
                                                                          raise_exceptions=False) else self.site.greyhound
            sections = page.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found')

            expected_next_races_name = self.next_races_title
            next_races = sections.get(expected_next_races_name, None)
            self.assertTrue(next_races, msg=f'*** There\'s no "{expected_next_races_name}" section')
            next_races.scroll_to()
            self.__class__._next_races = next_races

        return self._next_races

    @retry(stop=stop_after_attempt(3),
           retry=retry_if_exception_type((StaleElementReferenceException, TryAgain)),
           reraise=True)
    def get_event_from_next_races_module(self, event_name, raise_exceptions=True, timeout=1):
        page = self.site.horse_racing if self.site.wait_content_state('Horseracing', timeout=timeout,
                                                                      raise_exceptions=False) else self.site.greyhound
        self._logger.debug(f'*** Recognized "{page.__class__.__name__}" page')
        try:
            next_races = self.get_next_races_section()
            events = next_races.items_as_ordered_dict
            self.assertTrue(events, msg='No events were found in Next races section')
            event = events.get(event_name)
            if raise_exceptions:
                self.assertTrue(event, msg=f'Event "{event_name}" was not found in {list(events.keys())}')
                event.scroll_to()
                outcomes = event.items_as_ordered_dict
                self.assertTrue(outcomes, msg='No outcomes found')
        except VoltronException as e:
            self._logger.warning(e)
            if 'VoltronException' not in str(e):
                raise
            elif 'StaleElementReferenceException' in str(e):
                self.__class__._next_races = None
                raise StaleElementReferenceException(str(e))
            else:
                raise
        if not event and raise_exceptions:
            raise TryAgain
        return event

    # SiteServe requests
    @staticmethod
    def get_meetings_list_from_response(response):
        meetings_list_ss = []
        for event_resp in response:
            meetings_list_ss.append(event_resp['event']['typeName'].replace('|', '').strip())
        return sorted(list(set(meetings_list_ss)))

    @staticmethod
    def get_market_outcomes_from_response(response: dict, market_name: str) -> dict:
        """
        Having event response from Siteserve returns outcomes info for given market
        :param response: event response object (dictionary)
        :param market_name: name of market
        :return: outcomes info, in format {outcome_name: outcome_id}
        """
        if market_name:
            market = next((market_info['market'] for market_info in response['event']['children']
                           if market_name == market_info['market']['name']), None)
        else:
            market = response['event']['children'][0]['market']
        if not market:
            raise SiteServeException('Market not found for event with id: %s' % response['event']['id'])
        outcomes_info = {outcome_info['outcome']['name'].replace('|', ''): outcome_info['outcome']['id']
                         for outcome_info in market['children']}
        return outcomes_info

    def get_racing_event_with_form_details(self, star_rating=[], event_complete_info=False, distance=False,
                                           going=False, silk_availability=False, event_info=False,**kwargs):
        query_params_active_events = self.basic_active_events_filter()
        if kwargs.get('specials'):
            query_params_active_events.add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET,
                                                                              ATTRIBUTES.TEMPLATE_MARKET_NAME,
                                                                              OPERATORS.EQUALS,
                                                                              '|Racing Specials|')))
            active_events_list = self.ss_req.ss_event_to_outcome_for_class(query_builder=query_params_active_events)
            return active_events_list
        query_params_active_events.add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET,
                                                                                        ATTRIBUTES.TEMPLATE_MARKET_NAME,
                                                                                        OPERATORS.EQUALS,
                                                                                        '|Win or Each Way|')))
        active_events_list = self.ss_req.ss_event_to_outcome_for_class(query_builder=query_params_active_events)
        data_fabric = Datafabric()
        for event in active_events_list:
            event_id = event['event']['id']
            data = data_fabric.get_datafabric_data(event_id=event_id, raise_exceptions=False)
            if data['Error']:
                continue
            else:
                if data['document'][event_id]['horses']:
                    if len(star_rating) and not event_complete_info:
                        for form in data['document'][event_id]['horses']:
                            if form.get('starRating') is not None and form.get(
                                    'starRating') in star_rating and form.get('nonRunner') == "false":
                                return [event_id,
                                        {form.get('horseName'): form for form in data['document'][event_id]['horses']}]
                    if silk_availability:
                        for form in data['document'][event_id]['horses']:
                            if form.get('silk') is not None and form.get('silk'):
                                return [event_id,
                                        {form.get('horseName'): form for form in data['document'][event_id]['horses']}]
                    if event_complete_info and len(star_rating):
                        for form in data['document'][event_id]['horses']:
                            if form.get('starRating') is not None and form.get(
                                    'starRating') in star_rating and form.get('nonRunner') == "false":
                                return data['document']
                    if data['document'][event_id].get('distance') and data['document'][event_id].get('going') and distance and going:
                        return data['document']
                    if event_info:
                        return data['document']

        return None

    def get_event_details(self, **kwargs) -> namedtuple:
        """
        Gets event details of racing event based on keyword parameters (if any specified)
        :param kwargs: parameters used to filter events
        :return: event info details
        """
        # TODO VOL-1487
        event_id, details, data, rating_info_event_found, racing_post_verdict_event_found = None, None, None, None, None
        market_name = kwargs.get('market_name', '')
        query_params_active_events = self.basic_active_events_filter()\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.MARKET_STATUS_CODE, OPERATORS.EQUALS, 'A'))\
            .add_filter(simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'A'))

        if kwargs.get('forecast'):
            query_params_active_events.add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES,
                                                  OPERATORS.INTERSECTS, 'CF')))
        if kwargs.get('tricast'):
            query_params_active_events.add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES,
                                                  OPERATORS.INTERSECTS, 'TC')))
        if kwargs.get('cashout'):
            query_params_active_events.add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'))\
                                      .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')))
        if kwargs.get('each_way'):
            operator_val = OPERATORS.IS_TRUE if kwargs['each_way'] is True else OPERATORS.IS_FALSE
            query_params_active_events.add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, operator_val))
        if kwargs.get('race_form_info'):
            query_params_active_events.add_filter(racing_form(level=LEVELS.EVENT))
        if kwargs.get('gp'):
            gp_filter = simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_GP_AVAILABLE, OPERATORS.IS_TRUE)
            query_params_active_events.add_filter(gp_filter)
        active_events_list = self.ss_req.ss_event_to_outcome_for_class(query_builder=query_params_active_events)

        DetailsNamed = namedtuple("event_details", ["event_id", "event_name", "off_time", "type_name",
                                                    "event_date_time", "outcomes_info", "event_started",
                                                    "race_form_outcomes_info", "datafabric_data"])

        def details(event_id, event_name, off_time, type_name, event_date_time, outcomes_info,
                    event_started=None, race_form_outcomes_info=None, datafabric_data=None):
            return DetailsNamed(event_id, event_name, off_time, type_name, event_date_time, outcomes_info,
                                event_started, race_form_outcomes_info, datafabric_data)

        if kwargs.get('race_form_info'):
            if kwargs.get('df_event_summary', False):
                all_event_forms = [form for form in active_events_list if 'event' in form.keys() and 'UK' in form['event']['typeFlagCodes']]
            else:
                all_event_forms = [form for form in active_events_list if 'racingFormEvent' in form.keys()]
            if not all_event_forms:
                raise SiteServeException('No event with racing form found')
            racing_form_outcomes = []
            rating_info_event_found = False
            racing_post_verdict_event_found = False
            random.shuffle(all_event_forms)
            data_fabric = Datafabric()
            for event_form in all_event_forms:
                if kwargs.get('df_event_summary', False):
                    event_id = event_form.get('event').get('id')
                else:
                    event_id = event_form['racingFormEvent'].get('refRecordId')

                data = data_fabric.get_datafabric_data(event_id=event_id, raise_exceptions=False)
                if data['Error']:
                    continue

                if kwargs.get('racing_post_verdict'):
                    if all(key in data['document'][event_id] for key in
                           ['verdict', 'newspapers', 'courseGraphicsLadbrokes', 'horses']):
                        racing_post_verdict_event_found = True
                        break
                    else:
                        self._logger.warning('***Event with racing post verdict details not found ')
                        continue

                if kwargs.get('rating_info') and not data['Error']:
                    horses = data['document'][event_id]['horses']
                    if next((horse for horse in horses if horse.get('starRating', False)), False):
                        rating_info_event_found = True
                        break
                    else:
                        continue
            if data['Error']:
                raise ThirdPartyDataException('No event with racing information found. '
                                              'Can be due to receiving 404 error from datafabric.')
            elif not data['Error'] and kwargs.get('rating_info') and not rating_info_event_found:
                raise ThirdPartyDataException('No event with selections containing "starRating" property found.')
            elif not data.get('Error') and kwargs.get('racing_post_verdict') and not racing_post_verdict_event_found:
                raise ThirdPartyDataException('No event with selections containing "racing post verdict" details found.')

            found_event = self.ss_req.ss_event_to_outcome_for_event(
                event_id=event_id,
                query_builder=self.ss_query_builder
                .add_filter(racing_form(level=LEVELS.EVENT))
                .add_filter(racing_form(level=LEVELS.OUTCOME))
            )

            if not kwargs.get('df_event_summary', False):
                for outcome_form in found_event:  # do event to outcome for event with racing form outcome level
                    if 'racingFormOutcome' in outcome_form.keys():
                        racing_form_outcomes.append(outcome_form['racingFormOutcome'])
                if not racing_form_outcomes:
                    raise SiteServeException('No racing form for outcomes found')

            outcomes_info = self.get_market_outcomes_from_response(response=found_event[0],
                                                                   market_name=market_name)
            racing_form_outcomes_info = {}

            outcomes_info_items = outcomes_info.copy().items()
            for outcome_name, outcome_id in outcomes_info_items:
                for racing_form_outcome in racing_form_outcomes:
                    if outcome_id == racing_form_outcome['refRecordId']:
                        racing_form_outcomes_info[outcome_name] = racing_form_outcome
                        # delete from dict items with racing post info
                        # outcomes_info.pop(outcome_name, None)

            # update racing_form_outcomes_info dict with generic info for outcomes without racing post info for
            # example "Unnamed Favourite" and "Unnamed 2nd Favourite"
            for outcome_name in outcomes_info.keys():
                if 'Unnamed ' in outcome_name:
                    racing_form_outcomes_info[outcome_name] = 'generic'
            search = re.search(r'^(\d{1,2}:\d{2})(?:\s)', found_event[0]['event']['name'])
            off_time = search.group(1) if search else ''
            details_ = found_event[0]['event']['id'], found_event[0]['event']['name'], off_time, \
                found_event[0]['event']['typeName'], found_event[0]['event']['startTime'], outcomes_info, \
                True if found_event[0]['event'].get('rawIsOffCode', 'N') == 'Y' else False, racing_form_outcomes_info, \
                data['document'][event_id]
        else:
            if kwargs.get('gp'):
                found_event, gp_market = self.get_gp_event_from_resp(events=active_events_list, market_name=market_name)
                outcomes_info = {outcome_info['outcome']['name']: outcome_info['outcome']['id']
                                 for outcome_info in gp_market['market']['children']}
            else:
                found_event = next((event for event in active_events_list if 'event' in event.keys()), None)
                outcomes_info = self.get_market_outcomes_from_response(response=found_event, market_name=market_name)
            search = re.search(r'^(\d{1,2}:\d{2})(?:\s)', found_event['event']['name'])
            off_time = search.group(1) if search else ''
            details_ = found_event['event']['id'], found_event['event']['name'],\
                off_time, found_event['event']['typeName'], found_event['event']['startTime'], \
                outcomes_info,\
                True if found_event['event'].get('rawIsOffCode', 'N') == 'Y' else False
        return details(*details_)

    def get_gp_event_from_resp(self, events, market_name):
        """
        SS request returns events where either markets with GP are present or no markets at all,
        so this method looking for first entrance of event with BOG market
        :param events: response with events
        :param market_name: Needed market name, can be empty
        :return: Found event and it's market with GP
        """
        for event in events:
            markets = event.get('event', {}).get('children', {})
            for market in markets:
                if market.get('market', {}).get('isGpAvailable'):
                    if market_name and market.get('market', {}).get('name') != market_name:
                        continue
                    return event, market

        raise SiteServeException('There\'s no horse racing events with GP market')

    @staticmethod
    def get_outcomes_display_order_for_type(response):
        """
        :param response: event response from SiteServe
        :return: named tuple where markets_with_outcomes is a dict with all markets and outcomes info,
         market_names - list of market names, outcome_names - list of outcome names
        """
        market_outcomes = OrderedDict()
        market_outcome_data = {}
        for event in response:
            markets = event['event']['children'] if 'event' in event and 'children' in event['event'] else []
            for market in markets:
                outcomes = OrderedDict()
                ss_market_outcomes = market['market']['children'] if 'market' in market and 'children' in market['market'] else []
                for outcome in ss_market_outcomes:
                    market_name = market['market']['name']
                    outcome_name = outcome['outcome']['name']
                    outcome_price = 'SP' if not outcome['outcome'].get('children') else \
                        f"{outcome['outcome']['children'][0]['price']['priceNum']}" \
                        f"/{outcome['outcome']['children'][0]['price']['priceDen']}"
                    outcome_ = {outcome_name: outcome_price}
                    outcomes.update(outcome_)
                    market_outcome_data = {market_name: outcomes}
                market_outcomes.update(market_outcome_data) if market_name not in market_outcomes else market_outcomes[
                    market_name].update(outcomes)
        market_names = [market_name for market_name in market_outcomes]
        outcome_names = [outcome_name for market_name, outcome in market_outcomes.items() for outcome_name in outcome]
        parameters = namedtuple("parameters", ['markets_with_outcomes', 'market_names', 'outcome_names'])
        params = parameters(market_outcomes, market_names, outcome_names)
        return params

    def get_expected_event_distance(self, distance: str):
        """
        Get expected event distance from Datafabric response and converts it from yards to miles, furlongs and yards
        To convert yards into miles, furlongs and yards please do the following:
            *   A = 'distance'/1760 - whole number is **number of miles**
            *   B = 'distance' - A*1760
            *   C = B/220 - whole number is **number of furlongs**
            *   D = B - C*220 - **number of yards**
        If the distance is passed through as meters, we must convert to yards to do the calculation:
            *   1 meter = 1.09361 yards
        :return: string
        """
        if distance:
            distance = int(distance)
            distance_final = ''
            miles = distance // 1760
            part = distance - miles * 1760
            furlong = part // 220
            yards = part - furlong * 220
            for i, j in zip((miles, furlong, yards), ('m', 'f', 'y')):
                distance_final += f'{i}{j} ' if i else ''

            return distance_final.rstrip()
        else:
            return ''

    def get_edp_market_selections(self, market_name):
        self.site.racing_event_details.tab_content.event_markets_list.wait_item_appears(item_name=market_name, timeout=5)
        event_markets_list = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(event_markets_list, msg='No one market section found')
        self.assertIn(market_name, event_markets_list,
                      msg='No market "%s" section found in markets list: \n["%s"]'
                          % (market_name, '", "'.join(event_markets_list.keys())))
        market_selections = event_markets_list[market_name].items_as_ordered_dict
        self.assertTrue(market_selections, msg='No one market: "%s" selection found' % market_name)
        return market_selections

    def get_event_markets_ids(self, event_id):
        try:
            event_markets = self.ss_req.ss_event_to_outcome_for_event(event_id)[0]['event'][
                'children']
            return [event_market['market']['id'] for event_market in event_markets]
        except KeyError:
            raise SiteServeException('Can get event with id: "%s" available markets from SiteServe' % event_id)

    def get_event_market_selections_ids(self, event_id, market_id):
        try:
            event_markets = self.ss_req.ss_event_to_outcome_for_event(event_id)[0]['event']['children']
            market = next((event_market['market'] for event_market in event_markets
                           if int(event_market['market']['id']) == int(market_id)), None)
            return [market_selection['outcome']['id'] for market_selection in market['children']]
        except KeyError:
            raise SiteServeException('Can get event with id: "%s" available market with id: "%s" from SiteServe'
                                     % (event_id, market_id))

    def sort_selections_by_price(self, selections: list, prices: dict, non_runners: list) -> list:
        """
        Sorts selections by price.
        :param selections: list of selections names sorted by racecard
        :param prices: dict of prices, key is selection's race card number, value is a price
               note, that if class variable is passed here it's going to be changed
        :param non_runners: list of non-runner indexes
        :return: list of sorted selections
        """
        # Note: selection here is in fact number of selection
        if prices:
            for price in prices:
                if prices[price] and not isinstance(prices[price], float):
                    num, denom = prices[price].split('/')
                    prices[price] = float(num) / float(denom)

            non_runners_prices = {}
            sp_selections = list(filter(lambda index: prices[index] is None, prices))
            for selection in sp_selections:
                prices.pop(selection)
            for selection in non_runners:
                non_runners_prices[selection] = prices.pop(selection)
            reordered_prices = sorted(prices.items(), key=lambda kv: kv[1])
            for selection in sp_selections:
                reordered_prices.append((selection, None))
            for non_runner in non_runners:
                reordered_prices.append((non_runner, non_runners_prices[non_runner]))
            return [selections[price[0]] for price in reordered_prices]
        else:
            return selections

    def place_forecast_tricast_bet_from_event_details_page(self, sport_name='horse-racing', **kwargs):
        """
        Place foreacast or tricast bet on greyhounds or horse racing event details pages.
        :param sport_name: sport name horse-racing or greyhound-racing
        forecast = True if you need to place forecast bet. Forecast bet is placed by default
        tricast = True if you need to place tricast bet.
        any_button = True if you need to place forecast/tricast simple combination bet
        any_iteration_range = int value if you need to place complex combination bet
        :return: formatted string of selection names that should be displayed on betslip
        """
        any_iteration_range = kwargs.get('any_iteration_range')
        bet_button = None
        if sport_name == 'greyhound-racing':
            event_tab_content = self.site.greyhound_event_details.tab_content.event_markets_list
        elif sport_name == 'virtual-sports':
            event_tab_content = self.site.virtual_sports.tab_content.event_markets_list
        else:
            event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        if kwargs.get('forecast'):
            tab_name = vec.racing.RACING_EDP_FORECAST_MARKET_TAB
            iteration_range = range(0, 2)
            bet_button = 1
        if kwargs.get('tricast'):
            tab_name = vec.racing.RACING_EDP_TRICAST_MARKET_TAB
            iteration_range = range(0, 3)
            bet_button = 2
        if kwargs.get('any_button') and kwargs.get('any_iteration_range'):
            iteration_range = range(0, any_iteration_range)
        expected_selections = kwargs.get('expected_selections', None)
        if sport_name == 'virtual-sports':
            self.assertTrue(event_tab_content, msg='No outcome was found in section')
            selection_names = []
            for index in iteration_range:
                market_outcomes = event_tab_content.items_as_ordered_dict
                self.assertTrue('No outcomes for market')
                outcomes = list(market_outcomes.items())
                outcome_name, outcome = outcomes[index]
                selection_names.append(outcome_name)
                runner_buttons = outcome.items_as_ordered_dict
                self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{outcome_name}"')
                if kwargs.get('any_button'):
                    runner_bet_button = runner_buttons.get(vec.racing.CHECKBOXES.any)
                else:
                    runner_bet_button = list(runner_buttons.values())[index]
                self.assertTrue(runner_bet_button, msg=f'Runner bet button not found for "{outcome_name}"')
                runner_bet_button.click()
                if index == bet_button:
                    return selection_names
        else:
            event_tab_content.market_tabs_list.open_tab(tab_name)
            sections = wait_for_result(lambda: event_tab_content.items_as_ordered_dict,
                                       name='Racing content to appear',
                                       timeout=2,
                                       bypass_exceptions=(VoltronException, StaleElementReferenceException))
            self.assertTrue(sections, msg='No sections found for racing event tab')
            section_name, section = list(sections.items())[0]
            outcome_names = []
            for index in iteration_range:
                result = wait_for_result(lambda: section.items_as_ordered_dict.items(),
                                         name='Wait for outcomes to appear',
                                         timeout=5,
                                         bypass_exceptions=(VoltronException, StaleElementReferenceException))
                outcomes = list(result)
                self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')
                if expected_selections:
                    selection_presence = expected_selections[index] in [outcome[0] for outcome in outcomes]
                    if selection_presence:
                        outcome_name, outcome = next(_ for _ in outcomes if _[0] == expected_selections[index])
                    else:
                        raise VoltronException(f'Cannot find "{expected_selections[index]}" among '
                                               f'{[outcome[0] for outcome in outcomes]}')
                else:
                    outcome_name, outcome = outcomes[index]
                runner_buttons = wait_for_result(lambda: outcome.items_as_ordered_dict,
                                                 name='Wait for runner buttons to appear',
                                                 timeout=10,
                                                 bypass_exceptions=(VoltronException,
                                                                    StaleElementReferenceException))
                if None in runner_buttons.keys():
                    runner_buttons = wait_for_result(lambda: outcome.items_as_ordered_dict,
                                                     name='Wait for runner buttons to appear',
                                                     timeout=10,
                                                     bypass_exceptions=(VoltronException,
                                                                        StaleElementReferenceException))

                self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{outcome_name}"')
                if kwargs.get('any_button') and kwargs.get('forecast'):
                    index = 2
                elif kwargs.get('any_button') and kwargs.get('tricast'):
                    index = 3
                self._logger.info(f'*** Found runner buttons: "{runner_buttons}" and want to choose index "{index}"')
                runner_bet_button = list(runner_buttons.values())[index]
                runner_bet_button.click()
                outcome_names.append(outcome_name)
            self.assertTrue(event_tab_content.add_to_betslip_button.is_enabled(timeout=3), msg=f'"{vec.quickbet.BUTTONS.add_to_betslip}" button is not clickable')
            event_tab_content.add_to_betslip_button.click()
            if kwargs.get('any_button'):
                if kwargs.get('forecast'):
                    expected_selection_name = f'{outcome_names[0]}\n{outcome_names[1]}'
                if kwargs.get('tricast'):
                    expected_selection_name = f'{outcome_names[0]}\n{outcome_names[1]}\n{outcome_names[2]}'
                if kwargs.get('any_iteration_range'):
                    expected_selection_name = ''
                    for i in range(kwargs.get('any_iteration_range')):
                        expected_selection_name = f'{expected_selection_name}{outcome_names[i]}\n'
            else:
                if kwargs.get('forecast'):
                    expected_selection_name = f'1st.{outcome_names[0]}\n2nd.{outcome_names[1]}'
                if kwargs.get('tricast'):
                    expected_selection_name = f'1st.{outcome_names[0]}\n2nd.{outcome_names[1]}\n3rd.{outcome_names[2]}'
            return expected_selection_name

    def get_local_time_for_uk_tote(self, hours: int):
        """
        This method returns current time for timezone 'Europe/Kiev' or shifted time for other locations

        :param hours: specifies shifted time on hours
        :return: Current time depends on the location of the execution
        """
        # datetime.now() if str(get_localzone()) == 'Europe/Kiev' else datetime.now() - timedelta(hours=hours)
        # 26/06/2020: now it works on CI without delta
        local_time = datetime.now()
        return local_time

    def get_horse_info_from_datafabric(self, event_id: str, horse_name: str) -> dict:
        """
        Getting correct form id from datafabric
        event_id: ID of the racing event
        :return dict with horse information
        """
        horse_info = {}
        datafabric = Datafabric()
        data = datafabric.get_datafabric_data(event_id=event_id, raise_exceptions=True)
        horses = data['document'][event_id]['horses']
        for horse in horses:
            if horse['horseName'] == horse_name:
                horse_info = horse
                break
        return horse_info


class BaseGreyhound(BaseRacing):
    _ss_config = None

    @classmethod
    def get_ss_config(cls):
        if not cls._ss_config:
            ob_config = cls.get_ob_config()
            cls._ss_config = SiteServeRequests(env=tests.settings.backend_env,
                                               brand=cls.brand,
                                               category_id=ob_config.backend.ti.greyhound_racing.category_id,
                                               class_id=ob_config.backend.ti.greyhound_racing.class_ids
                                               )
        return cls._ss_config

    @classmethod
    def custom_setUp(cls, **kwargs):
        cls.get_ss_config()

    @property
    def category_id(self):
        return self.ob_config.backend.ti.greyhound_racing.category_id

    def get_event_details(self, **kwargs) -> namedtuple:
        """
        Gets event details of greyhound event based on keyword parameters (if any specified)
        :param kwargs: parameters used to filter events
        :return: event info details
        """
        # TODO VOL-1487
        event, event_id, data = None, None, None
        query_params_active_events = self.basic_active_events_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.MARKET_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CLASS_ID, OPERATORS.NOT_INTERSECTS, '201'))
        active_events_list = self.ss_req.ss_event_to_outcome_for_class(query_builder=query_params_active_events)
        DetailsNamed = namedtuple("event_details", ["event_id", "event_name", "off_time", "type_name", "type_id",
                                                    "event_date_time", "event_started", "distance", "grade", "verdict", "outcomes_info", "datafabric_data"])

        def details(event_id, event_name, off_time, type_name, type_id, event_date_time, event_started=None,
                    distance=None, grade=None, verdict=None, outcomes_info=None, datafabric_data=None):
            return DetailsNamed(event_id, event_name, off_time, type_name, type_id, event_date_time, event_started,
                                distance, grade, verdict, outcomes_info, datafabric_data)

        if kwargs.get('datafabric_data'):
            all_events = [event for event in active_events_list if 'event' in event.keys()]
            if not all_events:
                raise SiteServeException('No event with racing form found')

            for event in all_events:
                event_id = event['event']['id']
                data = Datafabric().get_datafabric_data(event_id=event_id, category_id=19, raise_exceptions=False)
                if data["Error"]:
                    continue
                break
            if data["Error"]:
                raise GeneralException('No event with racing information found. '
                                       'Can be due to receiving 404 error from datafabric.')

            datafabric_data = data['document'][event_id]
            search = re.search(r'^(\d{1,2}:\d{2})(?:\s)', event['event']['name'])
            off_time = search.group(1) if search else ''
            distance = datafabric_data.get('distance', False)
            outcomes_info = [{dog['dogName']: dog} for dog in datafabric_data['runners']]
            details_ = event['event']['id'], event['event']['name'], off_time, \
                event['event']['typeName'], event['event']['typeId'], event['event']['startTime'], \
                True if event['event'].get('rawIsOffCode', 'N') == 'Y' else False, distance[:-1] if distance else '', \
                datafabric_data.get('grade', ''), datafabric_data.get('verdict', ''), outcomes_info, datafabric_data

        elif kwargs.get('time_form_info'):
            t = TimeformClient(env=tests.settings.timeform)
            all_ids = t.get_races(count=500)
            if not all_ids:
                raise ThirdPartyDataException('No events with timeform found')

            active_events_ids = []
            for event_id in all_ids:
                ss_event = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id, raise_exceptions=False)
                if not ss_event:
                    continue
                ss_resp = ss_event[0]
                if ss_resp['event']['eventStatusCode'] == 'S':
                    continue
                if datetime.now() - datetime.strptime(ss_resp['event']['startTime'], self.ob_format_pattern) > timedelta(hours=3):
                    continue
                if 'event' in ss_resp:
                    is_resulted, is_finished = ss_resp['event'].get('isFinished', None), ss_resp['event'].get(
                        'isResulted', None)
                    if is_finished == 'true' or is_resulted == 'true':
                        continue
                    active_events_ids.append(event_id)
                    break
            if not active_events_ids:
                raise ThirdPartyDataException('No events with timeform found')

            for openbet_id in active_events_ids:
                form_info = t.get_race_info(openbet_id)
                if form_info:
                    break
            else:
                raise ThirdPartyDataException('No event with timeform found')

            distance, grade, verdict = form_info[0].get('raceDistance', ''), form_info[0].get('raceGradeName', ''), \
                form_info[0].get('verdict', '')
            ss_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=openbet_id)
            event_entry = ss_resp[0]['event']
            event_name = event_entry['name']
            is_event_started = True if event_entry.get('rawIsOffCode', 'N') == 'Y' else False
            search = re.search(r'^(\d{1,2}:\d{2})(?:\s)', event_name)
            off_time = search.group(1) if search else ''
            outcomes_info = []
            for outcome in form_info[0]['entries']:
                position_prediction = outcome.get('positionPrediction', '')
                name = outcome.get('greyHoundFullName', '')
                trainer_name_ = outcome.get('trainerFullName', '')
                search = re.search(r'([\w\s\'\-]+)\s(?:\([\w\s]+\))', trainer_name_)
                trainer_name = search.group(1) if search else ''
                star_rating = outcome.get('starRating', 0)
                status = outcome.get('statusName', '')
                one_line_comment_ = outcome.get('oneLineComment', '')
                one_line_comment = re.sub(' +', ' ', one_line_comment_).rstrip()
                outcomes_info.append({name: {'position_prediction': position_prediction,
                                             'trainer_name': trainer_name,
                                             'star_rating': star_rating,
                                             'status': status,
                                             'one_line_comment': one_line_comment}})

            details_ = openbet_id, event_name, off_time, event_entry['typeName'].replace('|', ''), \
                event_entry['typeId'], event_entry['startTime'], is_event_started, distance, grade, verdict, outcomes_info

        elif kwargs.get('racing_post_pick'):
            data_fabric = Datafabric()
            all_events = [event for event in active_events_list if 'event' in event.keys()]
            if not all_events:
                raise SiteServeException('No event with racing form found')

            for event in all_events:
                event_id = event['event']['id']
                data = data_fabric.get_datafabric_data(event_id=event_id, category_id=19, raise_exceptions=False)
                if data['Error']:
                    continue
                postpick = data['document'][event_id].get('postPick')
                if postpick:
                    break
            datafabric_data = data['document'][event_id]
            search = re.search(r'^(\d{1,2}:\d{2})(?:\s)', event['event']['name'])
            off_time = search.group(1) if search else ''
            distance = datafabric_data.get('distance', False)
            outcomes_info = [{dog['dogName']: dog} for dog in datafabric_data['runners']]
            details_ = event['event']['id'], event['event']['name'], off_time, \
                event['event']['typeName'], event['event']['typeId'], \
                event['event']['startTime'], True if event['event'].get('rawIsOffCode', 'N') == 'Y' else False, distance[:-1] if distance else '', \
                datafabric_data.get('grade', ''), datafabric_data.get('verdict', ''), outcomes_info, datafabric_data
        elif not kwargs.get('racing_post_pick'):
            data_fabric = Datafabric()
            all_events = [event for event in active_events_list if 'event' in event.keys()]
            if not all_events:
                raise SiteServeException('No event with racing form found')

            for event in all_events:
                event_id = event['event']['id']
                data = data_fabric.get_datafabric_data(event_id=event_id, category_id=19, raise_exceptions=False)
                if data['Error']:
                    break
            details_ = event['event']['id'], None, None, None, None, None, None, None, None, None, None, None
        else:
            query_params_active_events = self.ss_query_builder.add_filter(
                simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE,
                              OPERATORS.EQUALS, 'A'))
            active_events_list = self.ss_req.ss_event_to_outcome_for_class(query_builder=query_params_active_events)
            all_events = [event for event in active_events_list if 'event' in event.keys()]
            random_event = random.choice(all_events)
            search = re.search(r'^(\d{1,2}:\d{2})(?:\s)', random_event['event']['name'])
            off_time = search.group(1) if search else ''
            details_ = random_event['event']['id'], random_event['event']['name'], off_time, \
                random_event['event']['typeName'], random_event['event']['typeId'], \
                random_event['event']['startTime'], True if random_event['event'].get('rawIsOffCode', 'N') == 'Y' else False
        return details(*details_)

    def get_positions_prediction(self, outcomes_info):
        """
        :param outcomes_info: List of dictionaries
        :return: List of dictionaries sorted by position_prediction key, if position_prediction == 0, it goes to the end of list
        """
        sorted_by_pos = sorted(outcomes_info, key=lambda k: (list(k.values())[0]['position_prediction'] == 0,
                                                             list(k.values())[0]['position_prediction']))
        sorted_active = []
        for position in sorted_by_pos:
            if position[list(position.keys())[0]]['status'] != 'Dropped-Out':
                sorted_active.append(position)

        return sorted_active

    @property
    def uk_and_ire_type_name(self):
        if self.brand == 'bma':
            name = vec.sb.FLAG_UK
        else:
            if self.device_type == 'desktop':
                name = vec.sb.FLAG_UK_LONG
            else:
                name = get_racing_module_from_ws(category_id=self.category_id).get('title', vec.racing.UK_AND_IRE_TYPE_NAME)
                name = name.upper()
        return name


class BaseTote(BaseRacing):
    delete_events = False
    ss_req = None
    currency_codes = {
        'GBP': '£',
        'USD': '$',
        'EUR': '€',
        'SEK': 'Kr',
        'HKD': 'HK$',
        'AUD': 'AU$',
        'SGD': 'SGD$'
    }
    event_name_part = ['Fairview', 'Dundalk']
    correct_min_stake = 2.00
    correct_min_stake_HK = 10.00
    incorrect_min_stake = 0.05
    min_stake = 2.00
    min_stake_HK = 10.00
    total_stake = None
    active_pools = True
    market_ids = None

    @classmethod
    def pools_providers_query(cls):
        return query_builder().add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.PROVIDER, OPERATORS.IN, 'P,E,A,H,V'))

    @staticmethod
    def get_markets_ids(response):
        all_markets = []
        for entry in response:
            all_markets += entry['pool']['marketIds'].strip(',').split(',')
        return list(set(all_markets))

    @classmethod
    def get_ss_config(cls):
        if not cls._ss_config:
            ob_config = cls.get_ob_config()
            cls._ss_config = SiteServeRequests(env=tests.settings.backend_env,
                                               brand=cls.brand,
                                               category_id=ob_config.backend.ti.tote.category_id,
                                               class_id=ob_config.backend.ti.tote.horse_intl_thoroughbred_pools.class_id
                                               )
        return cls._ss_config

    @classmethod
    def custom_setUp(cls, **kwargs):
        cls.get_ss_config()
        cls.tote_ob_req = ToteOBConfig(env=tests.settings.backend_env, brand=cls.brand)
        if cls.active_pools:
            cls.pools_providers_query().add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.IS_ACTIVE, OPERATORS.IS_TRUE))
        cls.pools_providers_query().add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.IS_ACTIVE, OPERATORS.IS_TRUE))

        pools = cls.get_ss_config().ss_pool_for_class(query_builder=cls.pools_providers_query())
        cls.market_ids = cls.get_markets_ids(response=pools)
        cls.get_ss_config().ss_events_to_outcome_for_markets(market_ids=cls.market_ids, raise_exceptions=True)

    @classmethod
    def openTotePage(cls):
        if cls._site is None:
            cls.setUpSite()
            cls._device.open_url(url='%s%s' % (tests.HOSTNAME, '/tote'))
            cls._site.wait_splash_to_hide()

    @property
    def site(self):
        self.openTotePage()
        return self._site

    @classmethod
    def tearDownClass(cls):
        ob_config = cls.get_ob_config()
        events = ob_config.MODIFIED_EVENTS
        if cls.delete_events and (len(events) > 0):
            for event_id in events:
                ob_config.change_event_state(event_id=event_id)
        elif not cls.delete_events and len(events) > 0:
            for event_id in events:
                ob_config.change_event_state(event_id=event_id, displayed=True, active=True)
                ob_config.change_is_off_flag(event_id=event_id, is_off=False)
                cls.custom_tearDown()
        device = cls._device
        if device:
            if not cls.keep_browser_open:
                device.quit()
                return
            elif not tests.settings.allow_keep_open:
                device.quit()

    # TODO overridden because of https://jira.egalacoral.com/browse/BMA-31371: new url structure is not implemented for Tote
    def navigate_to_edp(self, event_id, sport_name=None, timeout=15):
        """
        Open created event using event id and direct link: https://<hostname>/event/event_id
        :param event_id: int or str
        :param sport_name: str optional page name for correct content state handling
        :param timeout: int
        :return: None
        """
        event_url = '%s/tote/event/%s' % (tests.HOSTNAME, event_id)
        self.device.navigate_to(event_url)
        self.site.wait_splash_to_hide(timeout=timeout)
        self._logger.info('***  Event details url is: %s' % self.device.get_current_url())
        if sport_name == 'horse-racing':
            content_state = 'RacingEventDetails'
        elif sport_name == 'greyhound-racing':
            content_state = 'GreyHoundEventDetails'
        elif sport_name == 'tote':
            content_state = 'ToteEventDetails'
        else:
            content_state = 'EventDetails'
        self.site.wait_content_state(state_name=content_state, timeout=timeout)

    def get_active_events(self, **kwargs):
        keywords = kwargs
        pool_query = self.pools_providers_query()
        market_query = self.ss_query_builder
        if kwargs.get('race_form_info'):
            market_query.add_filter(
                racing_form(LEVELS.EVENT)).add_filter(racing_form(LEVELS.OUTCOME))
        if kwargs.get('video_stream', None):
            market_query.add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.INTERSECTS, 'EVFLAG_GVM'))
        if kwargs.get('pool_type'):
            pool_query.add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.TYPE, OPERATORS.EQUALS, kwargs.get('pool_type')))
        pools = self.ss_req.ss_pool_for_class(query_builder=pool_query)
        self.market_ids = self.get_markets_ids(response=pools)
        is_active = keywords.get('is_active', True)
        if is_active:
            market_query.add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.IN, 'A'))\
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_FINISHED, OPERATORS.IS_EMPTY))\
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_RESULTED, OPERATORS.IS_EMPTY))\
                .add_filter(exists_filter(LEVELS.EVENT,
                                          simple_filter(LEVELS.MARKET, ATTRIBUTES.MARKET_STATUS_CODE, OPERATORS.EQUALS, 'A')))\
                .add_filter(exists_filter(LEVELS.EVENT,
                                          simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'A')))\
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_NAME, OPERATORS.NOT_EQUALS, 'Aqueduct'))\
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, self.end_date)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date_minus))
        events = self.ss_req.ss_events_to_outcome_for_markets(market_ids=self.market_ids, query_builder=market_query)
        return events

    @staticmethod
    def _make_list_unique(list):
        results = []
        for i in list:
            if not any([i[1] == one_tuple[1] for one_tuple in results]):
                results.append(i)
        return results

    def get_event_details(self, **kwargs) -> namedtuple:
        """
        Gets event details of international tote event based on keyword parameters (if any specified)
        :param kwargs: parameters used to filter events
        :return: event info details
        """
        # TODO VOL-1487
        active_events_list = self.get_active_events(**kwargs)
        if not active_events_list:
            raise SiteServeException('No active events found')
        for event in active_events_list:
            event_id = event['event']['id']
            market_id = event['event']['children'][0]['market']['id']\
                if event['event']['children'][0]['market']['name'] == 'Win' else ''
            if not market_id:
                continue
            search = re.search(r'Race \d (\d{2}:\d{2})', event['event']['name'])
            off_time = search.group(1) if search else ''
            country = event['event']['country']
            meeting_name = event['event']['typeName']
            selection_ids = {}
            selections = next((market['market']['children']
                               for market in event['event']['children']
                               if 'Win' in market['market']['name'] and market['market'].get('children')), None)
            for selection in selections:
                selection_ids.update({selection['outcome']['name']: selection['outcome']['id']})
            details = event_id, meeting_name, off_time, country, market_id, selection_ids
            break

        DetailsNamed = namedtuple("details", ["event_id", "meeting_name", "off_time", "country", "market_id", "selection_ids"])
        event_id = DetailsNamed(*details).event_id
        self.ob_config.MODIFIED_EVENTS.append(event_id)
        self._logger.info('*** Found Tote event with id "%s"' % event_id)
        return DetailsNamed(*details)

    def get_event_id_contains_video_stream(self):
        event_info = self.get_event_details(video_stream=True)
        return event_info

    def _get_event_ids_with_currency_code(self, currency_name, pool_type=('WN', 'PL', 'EX', 'TR')):
        pool_type = ','.join((pool_type,)) if isinstance(pool_type, str) else ','.join(pool_type)

        query = self.ss_query_builder\
            .add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.PROVIDER, OPERATORS.IN, 'P,E,A,H,V'))\
            .add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.TYPE, OPERATORS.IN, pool_type))

        pools = self.ss_req.ss_pool_for_class(query_builder=query)
        currency_to_market_ids = [pool['pool']['marketIds'].strip(',') for pool in pools
                                  if pool['pool']['currencyCode'] == currency_name]
        if not currency_to_market_ids:
            return None
        currency_to_market_ids = list(set(','.join(currency_to_market_ids).split(',')))
        start_date = f'{get_date_time_as_string(days=0)}T00:00:00.000Z'
        end_date = f'{get_date_time_as_string(days=1)}T00:00:00.000Z'
        query2 = self.ss_query_builder\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M'))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, start_date))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, end_date))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.ID, OPERATORS.IS_NOT_EMPTY))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_ACTIVE, OPERATORS.IS_TRUE))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_NAME, OPERATORS.NOT_EQUALS, 'Aqueduct'))
        events_to_outcome_for_markets = self.ss_req.ss_events_to_outcome_for_markets(market_ids=currency_to_market_ids,
                                                                                     query_builder=query2)
        events_ids = [event['event']['id'] for event in events_to_outcome_for_markets]

        return events_ids

    def get_event_id_with_currency_code(self, currency_name, all_events=False):
        events = self._get_event_ids_with_currency_code(currency_name=currency_name)
        if not events:
            return None
        return events if all_events else events[0]

    def get_pool_id(self, event_id: (int, str), pool_type: str = 'WN') -> str:
        """
        Knowing event id gets the id of corresponding pool
        :param event_id - id of event
        :param pool_type - pool type, one of WN (Win) - default, PL (Place), EX (Exacta), TR (Trifecta)
        :return id of pool that event_id belongs
        """
        query = self.ss_query_builder.add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.TYPE, OPERATORS.EQUALS, pool_type))
        pool_data = self.ss_req.ss_pool_for_event(event_id=event_id, query_builder=query)
        pool_id = pool_data[0]['pool']['id']
        return pool_id

    def get_pool_probable_values(self, pool_id: (int, str)) -> dict:
        """
        Get probable values for each runner in pool
        :param pool_id: id of pool
        :return: probable values for pool, e.g.: {runnerNumberId: poolValue}
        """
        pool = self.ss_req.ss_pool_to_pool_value(pool_id=pool_id)
        if 'children' in pool[0]['pool']:
            probable_values = {runner['poolValue']['runnerNumber1']: runner['poolValue']['value'] for runner in
                               pool[0]['pool']['children']}
            return probable_values
        return {}

    def get_stake_values_for_pool(self, event_id: (str, int), pool_type: str = 'WN') -> namedtuple:
        """
        Get stakes values: "minStakePerLine", "maxStakePerLine", "minTotalStake", "maxTotalStake"
        :param event_id: Tote event id
        :param pool_type: one of WN (Win) - default, PL (Place), EX (Exacta), TR (Trifecta)
        :return: named tuple of floats (stakes values: "minStakePerLine", "maxStakePerLine", "minTotalStake", "maxTotalStake")
        Note: Extra wrapper is created to cover cases where's needed to use same method in classmethod and test itself
        """
        return self._get_stake_values_for_pool(event_id=event_id, pool_type=pool_type)

    @classmethod
    def _get_stake_values_for_pool(cls, event_id: (str, int), pool_type: str = 'WN') -> namedtuple:
        """
        Get stakes values: "minStakePerLine", "maxStakePerLine", "minTotalStake", "maxTotalStake"
        :param event_id: Tote event id
        :param pool_type: one of WN (Win) - default, PL (Place), EX (Exacta), TR (Trifecta)
        :return: named tuple of floats (stakes values: "minStakePerLine", "maxStakePerLine", "minTotalStake", "maxTotalStake")
        """
        ss_query_builder = query_builder().add_filter(translation_lang())
        query = ss_query_builder.add_filter(
            simple_filter(LEVELS.POOL, ATTRIBUTES.TYPE, OPERATORS.EQUALS, pool_type))
        pools = cls.get_ss_config().ss_pool_for_event(event_id=event_id, query_builder=query)
        try:
            stakes = next(((
                float(pool['pool']['minStakePerLine']),
                float(pool['pool']['maxStakePerLine']),
                float(pool['pool']['minTotalStake']),
                float(pool['pool']['maxTotalStake']),
                float(pool['pool']['stakeIncrementFactor']))
                for pool in pools), (0, 0, 0, 0, 0))
            StakesNamed = namedtuple("stakes", ["minStakePerLine", "maxStakePerLine", "minTotalStake", "maxTotalStake",
                                                "stakeIncrementFactor"])
            return StakesNamed(*stakes)
        except Exception as e:
            raise SiteServeException(message=e)

    def get_pool_currency(self, event_id: (int, str), pool_type: str = 'WN') -> str:
        """
        Having international tote event returns currency for given pool type
        :param event_id: id of event
        :param pool_type: pool type, one of WN (Win) - default, PL (Place), EX (Exacta), TR (Trifecta)
        :return:
        """
        query = self.ss_query_builder.add_filter(
            simple_filter(LEVELS.POOL, ATTRIBUTES.TYPE, OPERATORS.EQUALS, pool_type))
        pool = self.ss_req.ss_pool_for_event(event_id=event_id, query_builder=query)
        try:
            pool_currency = pool[0]['pool']['currencyCode']
        except Exception as e:
            raise SiteServeException(message=e)
        return pool_currency

    def get_expected_event_distance(self, event_id: (int, str)) -> str:
        """
        Get event distance
        To convert yards into miles, furlongs and yards please do the following:
            *   A = 'distance'/1760 - whole number is **number of miles**
            *   B = 'distance' - A*1760
            *   C = B/220 - whole number is **number of furlongs**
            *   D = B - C*220 - **number of yards**
        If the distance is passed through as meters, we must convert to yards to do the calculation:
            *   1 meter = 1.09361 yards
        :param event_id: id of international tote event
        :return: event distance string
        """
        query = self.ss_query_builder.add_filter(racing_form(LEVELS.EVENT)).add_filter(racing_form(LEVELS.OUTCOME))
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id, query_builder=query)
        form_data = [data for data in resp if 'racingFormEvent' in data]
        racing_form_event = form_data[0].get('racingFormEvent')
        if not racing_form_event:
            raise SiteServeException('Event does not have racing form data')
        event_distance = racing_form_event['distance']
        if event_distance:
            match_group = re.match(r'Yards,(\d+)', event_distance).group(1)
            distance = int(match_group) if match_group else 0
            miles = distance // 1760
            part = distance - miles * 1760
            furlong = part // 220
            yards = part - furlong * 220
            return '%sm %sf %sy' % (miles, furlong, yards)
        else:
            return ''

    def set_status_of_tote_pool(self, customer_username, outcome_bet_receipt_bet_id, bet_winnings, set_status):
        Parameters = namedtuple("tote_status",
                                ["customer_username", "outcome_bet_receipt_bet_id", "bet_winnings", "set_status"])
        tote_statuses = Parameters(customer_username, outcome_bet_receipt_bet_id, bet_winnings, set_status)
        return self.tote_ob_req.find_bets(tote_statuses.customer_username,
                                          tote_statuses.outcome_bet_receipt_bet_id,
                                          tote_statuses.bet_winnings,
                                          tote_statuses.set_status)

    def tap_on_pool_type(self, pool_type):
        """
        On Event Details page tap on Pool type
        """
        self.site.tote_event_details.tab_content.grouping_buttons.click_button(pool_type)
        current_group_button = self.site.tote_event_details.tab_content.grouping_buttons.current
        self.assertEqual(current_group_button, pool_type,
                         msg='Incorrect default grouping: current "%s", while expected "%s"'
                             % (current_group_button, pool_type))

    def get_pool_size(self, event_id: (str, int), pool_type: str = 'WN') -> float:
        """
        Get size of pool
        :param event_id: Tote event id
        :param pool_type: one of WN (Win) - default, PL (Place), EX (Exacta), TR (Trifecta)
        :return: float - pool size
        """
        pools = self.ss_req.ss_pool_for_event(event_id=event_id)
        pool_size = next((float(pool['pool']['poolValue']) for pool in pools
                          if pool['pool']['type'] == pool_type and 'poolValue' in pool['pool']), None)
        return pool_size

    def check_pool_size(self, currency_code, currency_sign, expected_pool_size):
        """
        Check pool size
        """
        pool_size_label = self.site.tote_event_details.tab_content.pool_size_label
        self.assertEqual(pool_size_label, 'Prize pool')

        exchange_rate = self.exchange_rates[currency_code]
        expected_user_currency_pool_size = expected_pool_size / exchange_rate
        user_currency_pool_size = self.site.tote_event_details.tab_content.user_currency_pool_size
        if currency_sign != self.user_currency_sign:
            pool_currency_pool_size = self.site.tote_event_details.tab_content.pool_currency_pool_size
            self.assertAlmostEqual(float(pool_currency_pool_size), expected_pool_size, delta=0.01)
        self.assertAlmostEqual(float(user_currency_pool_size), expected_user_currency_pool_size, delta=0.01)

    def check_pool_probable_values(self, expected_probable_values):
        """
        Check pool probable values
        """
        sections = self.site.tote_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No Sections found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No Outcomes found')
        for i in range(0, len(outcomes.values())):
            outcome = list(outcomes.values())[i]
            self._logger.debug('*** Outcome "%s", guide "%s"' % (outcome.horse_name, outcome.guide))
            self.assertAlmostEqual(float(outcome.guide), float(expected_probable_values[str(i + 1)]), delta=0.01)  # key is the runner number which starts from 1

    def place_single_pool_bet(self):
        """
        Place a bet on at least one selection
        """
        bpp_config = BPPConfig()
        pool_currency = 'GBP' if not self.pool_currency else self.pool_currency
        tote_events_sections_list = self.site.tote_event_details.tab_content.event_markets_list
        sections = tote_events_sections_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No Sections found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No Outcomes found')
        outcome = next((outcome for outcome_name, outcome in outcomes.items()
                        if not outcome.is_non_runner and outcome.stake.is_enabled()), None)
        self.assertIsNotNone(outcome, msg='No active outcomes found')
        self._logger.debug('*** Outcome: {0} '.format(outcome.horse_name))
        min_stake = self.min_stake_HK if pool_currency == 'HKD' else self.min_stake
        outcome.enter_stake(int(min_stake))
        total_stake = tote_events_sections_list.betslip_bet_container.total_stake
        self.__class__.total_stake = float(total_stake.amount)
        self.__class__.total_stake_converted = float(total_stake.converted_amount)
        self.assertAlmostEqual(self.total_stake, float(min_stake), delta=0.01,
                               msg='The value of total stake field is not correct, expected "%s" but found "%s"'
                                   % (self.total_stake, float(min_stake)))

        if self.site.wait_logged_in(timeout=1):
            # for not logged in user converted amount is not shown, else clause is covered in lines 739 - 743
            self.__class__.total_stake = float(total_stake.converted_amount)
            exchange_rates = bpp_config.get_currency_exchange_rates(currency_code=pool_currency)
            converted_min_stake = min_stake / float(exchange_rates)
            self.assertAlmostEqual(float(total_stake.converted_amount), converted_min_stake, delta=0.01,
                                   msg='The value of converted total stake field is not correct, expected "%s" but found "%s"'
                                       % (converted_min_stake, float(total_stake.converted_amount)))

    def place_multiple_pool_bet(self, number_of_selections=3):
        bpp_config = BPPConfig()
        pool_currency = 'GBP' if not self.pool_currency else self.pool_currency
        tote_events_sections_list = self.site.tote_event_details.tab_content.event_markets_list
        sections = tote_events_sections_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No Sections found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No Outcomes found')
        min_stake = self.min_stake_HK if pool_currency == 'HKD' else self.min_stake
        counter = 0
        for outcome_name, outcome in outcomes.items():
            if counter >= number_of_selections:
                break
            if outcome.is_non_runner or not outcome.stake.is_enabled():
                continue
            self._logger.debug('*** Outcome: {0} '.format(outcome_name))
            outcome.enter_stake(int(min_stake))
            counter += 1
        self.assertEqual(counter, number_of_selections, msg='Number of added outcomes %s in less than expected %s'
                         % (counter, number_of_selections))
        total_stake = tote_events_sections_list.betslip_bet_container.total_stake
        self.__class__.total_stake = float(total_stake.amount)
        self.__class__.total_stake_converted = float(total_stake.converted_amount)
        self.assertAlmostEqual(self.total_stake, min_stake * counter, delta=0.01,
                               msg='The value of total stake field is not correct, expected "%s" but found "%s"'
                                   % (min_stake * counter, self.total_stake))
        if self.site.wait_logged_in(timeout=1):
            exchange_rates = bpp_config.get_currency_exchange_rates(currency_code=pool_currency)
            converted_min_stake = min_stake / float(exchange_rates)
            self.assertAlmostEqual(float(total_stake.converted_amount), converted_min_stake * 3, delta=0.01,
                                   msg='The value of converted total stake field is not correct, expected "%s" but found "%s"'
                                       % (converted_min_stake * 3, float(total_stake.converted_amount)))
            self.__class__.total_stake = float(total_stake.converted_amount)

    def verify_tote_betreceipt_success_message(self):
        success_text = self.site.tote_event_details.tab_content.bet_receipt_section_list.success_message_text
        expected_messages = [vec.tote.SUCCESS_BET_RECEIPT_MSG, vec.tote.SUCCESS_BETS_RECEIPT_MSG]
        self.assertIn(success_text, expected_messages,
                      msg=f'Success message "{success_text}" is not shown in "{expected_messages}"')
