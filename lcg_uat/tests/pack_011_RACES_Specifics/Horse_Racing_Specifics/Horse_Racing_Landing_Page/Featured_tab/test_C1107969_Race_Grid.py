import collections
import datetime
import re
from random import randint

import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.utils.date_time import get_date_time_as_string

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-55910')
@vtest
class Test_C1107969_Race_Grid(BaseRacing):
    """
    TR_ID: C1107969
    NAME: Race Grid
    DESCRIPTION: This test case verifies Race grid on Featured tab for Horse Racing
    PRECONDITIONS: * Coral app is loaded
    PRECONDITIONS: In order to get a list with Class IDs use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:YY&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Where:
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * YY - category id (Horse Racing category id =21)
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: To retrieve all events for class id identified in step 1 use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:YY&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Where:
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * YYYY is a comma separated list of Class id's(e.g. 97 or 97, 98);
    PRECONDITIONS: * YY - sport category id (Horse Racing category id = 21)
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: Parameter **typeName** defines 'Race Meetings' name
    PRECONDITIONS: Parameter 'startTime' defines event start time (note, this is not a race local time)
    """
    keep_browser_open = True
    start_date = f'{get_date_time_as_string(date_time_obj=datetime.date.today(), days=0, hours=1, time_format="%Y-%m-%dT%H:%M:%S.000Z")}'

    @property
    def basic_query_params(self):
        return self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'UK,IE')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.NOT_INTERSECTS, 'SP')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.NAME, OPERATORS.NOT_EQUALS, '%7Cnull%7C')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.NOT_CONTAINS, 'EVFLAG_AP')) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.NOT_INTERSECTS, 'MKTFLAG_SP')))

    def get_events(self):
        query_params = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, self.ob_config.backend.ti.horse_racing.category_id)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'UK,IE,FR,AE,ZA,IN,US,AU,CL,INT,VR')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.NOT_INTERSECTS, 'SP')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date_minus)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CLASS_ID, OPERATORS.NOT_INTERSECTS, '227')) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.NOT_INTERSECTS, 'MKTFLAG_SP'))) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.NOT_CONTAINS, 'EVFLAG_AP')))
        return self.ss_req_hr.ss_event_to_outcome_for_class(query_builder=query_params)

    @staticmethod
    def sort_events_by_type(response):
        events_from_response = {'UK': [], 'IE': [], 'FR': [], 'IN': [], 'AE': [], 'CL': [], 'AU': [], 'US': [],
                                'ZA': [], 'INT': [], 'VR': []}
        events_with_outcomes = []
        for event in response:
            if event['event'].get('children'):
                markets = event['event'].get('children')
                for market in markets:
                    if market.get('market').get('children'):
                        events_with_outcomes.append(event)
                        break

        all_events = []
        for event in events_with_outcomes:
            if event['event'].get('typeFlagCodes'):
                flag_codes = event['event'].get('typeFlagCodes').split(',')[:-1]
                for flag in flag_codes:
                    if flag in events_from_response.keys():
                        if event['event']['typeName'] not in all_events:
                            events_from_response[flag].append(event['event']['typeName'])
                            all_events.append(event['event']['typeName'])
                        break

        events_from_response['UK,IE'] = events_from_response['UK']
        events_from_response['UK,IE'].extend(events_from_response['IE'])

        del events_from_response['UK']
        del events_from_response['IE']

        return events_from_response

    def get_expected_race_grid_accordions(self):
        expected_race_grid_accordions = []
        meetings = self.sort_events_by_type(self.get_events())
        for meeting_code in meetings:
            if meetings[meeting_code]:
                accordion = self.type_flag_codes[meeting_code] \
                    if self.device_type == 'desktop' and self.brand != 'ladbrokes' else self.type_flag_codes[meeting_code].upper()
                expected_race_grid_accordions.append(accordion)
        return expected_race_grid_accordions

    def compare_ui_events_with_ss_response(self, resp):
        meetings_events_ss, meetings_events_ui = collections.defaultdict(list), collections.defaultdict(list)

        meetings_list_ss = self.get_meetings_list_from_response(response=resp)
        self._logger.debug(f'*** SiteServe Response: Meetings list: "{meetings_list_ss}"')

        for meeting in meetings_list_ss:
            for event_resp in resp:
                if event_resp['event']['typeName'].strip() == meeting:
                    search = re.search(r'([\d:]+)', event_resp['event']['name'])
                    event_time = search.group(1) if search else ''
                    meetings_events_ss[meeting].append(event_time)

        meetings_events_ss = [{key.upper(): sorted(value)} for key, value in meetings_events_ss.items()]
        meetings_events_ss = sorted(meetings_events_ss, key=lambda d: sorted(d.items()))

        self._logger.debug(f'*** SiteServe Response: List of events in each meeting: "{meetings_events_ss}"')

        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        section = sections[self.uk_and_ire_type_name]
        section.expand()
        self.assertTrue(section.is_expanded(), msg=f'Section "{self.uk_and_ire_type_name}" is not expanded')

        meetings_list_ui = section.items_as_ordered_dict
        self.assertTrue(meetings_list_ui, msg=f'No meetings found in "{self.uk_and_ire_type_name}"')

        self._logger.debug(f'*** Horse Racing page: Meetings list: "{list(meetings_list_ui.keys())}"')

        meetings_list_ui_sorted = sorted(list(meetings_list_ui.keys()))
        meetings_list_ss_sorted = sorted([meeting.upper() for meeting in meetings_list_ss])

        if self.brand == 'ladbrokes':
            meetings_list_ui_sorted = [meeting.upper() for meeting in meetings_list_ui_sorted]

        for date_tab_name in meetings_list_ss_sorted:
            self.assertIn(date_tab_name, meetings_list_ss_sorted,
                          msg=f'\nMeetings list on UI: \n:"{date_tab_name}", '
                              f'\nMeetings list from SiteServe: \n"{meetings_list_ss_sorted}"')

        for meeting_name, meeting in meetings_list_ui.items():
            events = meeting.items_as_ordered_dict
            meeting_name = meeting_name.upper()
            self.assertTrue(events, msg=f'No events found for meeting "{meeting_name}"')
            meetings_events_ui[meeting_name] = events.keys()

        meetings_events_ui = [{key: sorted(value)} for key, value in meetings_events_ui.items()]
        meetings_events_ui = sorted(meetings_events_ui, key=lambda d: sorted(d.items()))

        self._logger.debug(f'*** Horse Racing page: List of events in each meeting: "{meetings_events_ui}"')

        # BMA-55910
        # self.assertListEqual(meetings_events_ui, meetings_events_ss,
        #                      msg=f'\nMeetings events list on UI: \n:"{meetings_events_ui}", '
        #                          f'\nMeetings events list from SiteServe: \n"{meetings_events_ss}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create UK & IRE, International and Virtual events
        EXPECTED: Events are created
        """
        self.__class__.ss_req_hr = SiteServeRequests(env=tests.settings.backend_env,
                                                     class_id=self.horse_racing_live_class_ids,
                                                     category_id=self.ob_config.backend.ti.horse_racing.category_id,
                                                     brand=self.brand)
        off_time = randint(1, 1000)
        tomorrow = self.get_date_time_formatted_string(days=1)
        self.ob_config.add_UK_racing_event(number_of_runners=1, off_time=off_time)
        self.ob_config.add_UK_racing_event(number_of_runners=1, start_time=tomorrow)
        self.ob_config.add_international_racing_event(number_of_runners=1)
        self.ob_config.add_virtual_racing_event(number_of_runners=1)

    def test_001_navigate_to_hr_featured_tab(self):
        """
        DESCRIPTION: Navigate to HR -> Featured tab
        EXPECTED: Race Grid accordions (expanded by default) are displayed in the following order:
        EXPECTED: * UK & IRE (events with typeFlagCodes 'UK' or 'IE')
        EXPECTED: * International (events with typeFlagCodes 'INT')
        EXPECTED: * Virtual (events with typeFlagCodes 'VR')
        EXPECTED: It is possible to collapse/expand accordions by tapping section header
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Current tab "{current_tab}" is not the same as expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')

        other_international = [vec.racing.USA_TYPE_NAME,
                               vec.racing.CHILE_TYPE_NAME,
                               vec.racing.UAE_TYPE_NAME,
                               vec.racing.INDIA_TYPE_NAME,
                               vec.racing.CHILE_TYPE_NAME,
                               vec.racing.FRANCE_TYPE_NAME,
                               vec.racing.SOUTH_AFRICA_TYPE_NAME,
                               vec.racing.AUSTRALIA_TYPE_NAME]

        sections_to_exclude = [self.next_races_title,
                               self.enhanced_races_name,
                               vec.racing.ENHANCED_MULTIPLES_NAME,
                               vec.racing.YOURCALL_SPECIALS.upper(),
                               self.international_tote_type_name,
                               self.virtual_type_name]

        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.sections = {section_name: section for section_name, section in sections.items()
                                   if section_name.lower() not in [_.lower() for _ in other_international + sections_to_exclude]}

        expected_accordions_from_resp = self.get_expected_race_grid_accordions()
        expected_accordions_from_resp = [section for section in expected_accordions_from_resp
                                         if section.lower() not in [_.lower() for _ in other_international]]

        expected_accordions_order = self.get_order_of_modules()
        expected_accordions_order = [accordion.upper() for accordion in expected_accordions_order
                                     if accordion.lower() not in [_.lower() for _ in sections_to_exclude]]
        actual_accordions_order = [accordion.upper() for accordion in list(self.sections.keys())]
        final_list = [x for _, x in sorted(zip(expected_accordions_from_resp, expected_accordions_order), key=lambda pair: pair[0])]

        self.assertListEqual(actual_accordions_order, expected_accordions_order,
                             msg=f'Incorrect racing accordions are displayed.\n'
                             f'Actual: "{list(self.sections.keys())}\nExpected: "{expected_accordions_order}"')
        self.assertEqual(list(self.sections.keys())[0], self.uk_and_ire_type_name,
                         msg=f'"{self.uk_and_ire_type_name}" accordion should be displayed first. '
                             f'Currently first one is "{list(self.sections.keys())[0]}"')
        last_final_item = final_list[-1]
        last_section_item = list(self.sections.keys())[-1]
        self.assertEqual(last_section_item.lower(), last_final_item.lower(),
                         msg=f'"{last_final_item.lower()}" accordion should be displayed last. '
                         f'Currently last one is "{last_section_item.lower()}"')

        for section_name, section in self.sections.items():
            section.scroll_to()
            section.expand()
            self.assertTrue(section.is_expanded(timeout=2),
                            msg=f'Section "{section_name}" is not expanded')
            section.collapse()
            self.assertFalse(section.is_expanded(expected_result=False, timeout=2),
                             msg=f'Section "{section_name}" is not collapsed')

    def test_002_verify_race_grid_accordions_content(self):
        """
        DESCRIPTION: Verify Race Grid accordions content
        EXPECTED: * Day tabs
        EXPECTED: * List of Race meeting sections for first day tab
        """
        self.assertIn(self.uk_and_ire_type_name, self.sections)
        self.__class__.section = self.sections[self.uk_and_ire_type_name]
        self.section.expand()
        self.assertTrue(self.section.is_expanded(), msg=f'Section "{self.uk_and_ire_type_name}" is not expanded')

    def test_003_verify_day_tabs(self):
        """
        DESCRIPTION: Verify day tabs
        EXPECTED: * Day tab name is day of the week
        EXPECTED: * when up to 3 days tabs available complete days name are displayed (ex. WEDNESDAY, THURSDAY)
        EXPECTED: * ***Coral*** when more than 3 days tabs available abbreviations for the days are displayed (ex. WED, THU, FRI..)
        EXPECTED: * ***Ladbrokes*** when more than 3 tabs - complete days name (according to https://app.zeplin.io/project/5c35cf920695502973380b86/screen/5c3cb9a10695502973712579)
        EXPECTED: * Day tabs are sorted chronologically
        EXPECTED: * If there are no events for day tab, tab is not shown
        EXPECTED: * First day tab (corresponding to the earliest day) is opened by default
        """
        all_day_tabs = list(self.section.date_tab.items_as_ordered_dict.keys())[0]
        for date_tab_name, _ in self.section.date_tab.items_as_ordered_dict.items():
            self.assertIn(date_tab_name.upper(), vec.racing.DAYS,
                          msg=f'Actual tab days "{all_day_tabs}" does not match expected "{vec.racing.DAYS}')
        self.assertEqual(all_day_tabs.upper(), vec.racing.DAYS[0],
                         msg=f'Current day tab "{all_day_tabs.upper()}" is not the same as expected "{vec.racing.DAYS[0]}"')

    def test_004_verify_amount_of_tabs(self):
        """
        DESCRIPTION: Verify amount of tabs
        EXPECTED: * UK & IRE and International: up to 6 next day tabs are present if available
        EXPECTED: * Virtual (Ladbrokes/Coral Legends): up to 2 day tabs corresponding to Today and Tomorrow days are present if available
        """
        for section_name, section in self.sections.items():
            section.scroll_to()
            section.expand()
            self.assertTrue(section.is_expanded(timeout=2), msg=f'Section "{section_name}" is not expanded')
            tabs_count = len(section.date_tab.items_as_ordered_dict)
            if section_name in [self.uk_and_ire_type_name, self.international_type_name]:
                self.assertTrue(tabs_count <= 6,
                                msg=f'Day tabs count "{tabs_count}" '
                                    f'is not equal or less than 6 in section "{section_name}"')
            elif section_name == self.legends_type_name:
                self.assertTrue(tabs_count <= 2,
                                msg=f'Day tabs count "{tabs_count}" is not equal or less than 2 in section "{section_name}"')

    def test_005_verify_content_for_first_day_tab(self):
        """
        DESCRIPTION: Verify content for first day tab
        EXPECTED: * All events from SS response with start time (**startTime** attribute) corresponding to selected day tab are displayed within corresponding type (race meeting) section
        """
        query_params_today = self.basic_query_params \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, self.end_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date_minus))

        resp = self.ss_req_hr.ss_event_to_outcome_for_class(class_id=[16323, 16322, 228, 226, 224, 223],
                                                            query_builder=query_params_today)
        self.compare_ui_events_with_ss_response(resp=resp)

    def test_006_click_successively_on_all_other_future_day_tabs_and_repeat_step_5(self):
        """
        DESCRIPTION: Click successively on all other future day tabs and repeat step #5
        EXPECTED: Result is the same
        """
        all_day_tabs = self.section.date_tab.items_as_ordered_dict
        self.assertTrue(len(all_day_tabs) > 1, msg='Only one date tab found')
        second_tab_name, second_tab = list(all_day_tabs.items())[1]
        second_tab.click()
        result = wait_for_result(lambda: self.section.date_tab.current_date_tab == second_tab_name,
                                 name='Other future day tab is opened',
                                 timeout=3)
        self.assertTrue(result, msg=f'Current day tab "{self.section.date_tab.current_date_tab}" '
                                    f'is not the same as expected "{second_tab_name}"')

        start_date = f'{get_date_time_as_string(date_time_obj=datetime.date.today(), days=1, time_format="%Y-%m-%dT%H:%M:%S.000Z")}'
        end_date = f'{get_date_time_as_string(date_time_obj=datetime.date.today(), days=2, time_format="%Y-%m-%dT%H:%M:%S.000Z")}'

        query_params_tomorrow = self.basic_query_params \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, end_date)) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.TEMPLATE_MARKET_NAME,
                                                                  OPERATORS.EQUALS, '|Win or Each Way|')))

        resp = self.ss_req_hr.ss_event_to_outcome_for_class(class_id=[16323, 16322, 228, 226, 224, 223],
                                                            query_builder=query_params_tomorrow)
        self.compare_ui_events_with_ss_response(resp=resp)
