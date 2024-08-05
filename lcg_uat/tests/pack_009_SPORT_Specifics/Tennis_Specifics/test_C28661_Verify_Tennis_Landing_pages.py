import time
from datetime import datetime

import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests, exists_filter
from crlat_siteserve_client.utils.date_time import get_date_time_as_string

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.sports
@pytest.mark.tennis
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.timeout(800)
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28661_Verify_Landing_pages(BaseSportTest):
    """
    TR_ID: C28661
    NAME: Verify Tennis Landing pages
    DESCRIPTION: This test case verifies Tennis Landing pages
    DESCRIPTION: **Autotests:**
    DESCRIPTION: Mobile - [C9690158](https://ladbrokescoral.testrail.com/index.php?/cases/view/9690158)
    DESCRIPTION: Desktop - [C9697897](https://ladbrokescoral.testrail.com/index.php?/cases/view/9697897)
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID (Tennis=34)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    max_number_of_sections = 4
    expected_events_order = []
    outright_events_order = []
    tomorrow_events_order = []
    future_events_order = []

    def verify_events_are_present(self, resp):
        event = next((event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')), None)
        if not event:
            raise SiteServeException(
                f'No active events found for category id "{self.ob_config.backend.ti.tennis.category_id}"')

    def get_event_start_time(self, league: str, sports_list: list) -> dict:
        """
        Gets events start times
        :param sports_list: list of all sports
        :param league: str league name
        :return: return dictionary where key is name and value is event startTime
        """
        events = [event['event'] for event in sports_list if event['event']['typeName'].upper() in league.upper()]
        return {x['name']: x['startTime'] for x in events}

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by type typeDisplayOrder in ascending order otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        sport_categories = {f"{sport['event']['categoryName']} - {sport['event']['typeName']}":
                            int(sport['event']['typeDisplayOrder']) for sport in sports_list}
        return sorted(sport_categories, key=lambda k: (sport_categories[k], k))

    def get_order_of_events(self, league: str, sports_list: list) -> list:
        """
        Having response gets the expected order of events in coupon
        :param league: str league name
        :param sports_list: list of all sports
        :return: expected order of events in league
        """
        if league:
            event_start_times = self.get_event_start_time(league=league, sports_list=sports_list)
        else:
            event_start_times = {x['event']['name']: x['event']['startTime'] for x in sports_list}

        event_start_times_converted = []
        for name, start_time in event_start_times.items():
            date_time_obj = datetime.strptime(start_time.split(',')[0], self.ob_format_pattern)
            event_start_times_converted.append((name, date_time_obj.timetuple()))

        expected_order_tuple = sorted(event_start_times_converted, key=lambda x: (x[1], x[0]))
        return [x for x, _ in expected_order_tuple]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create tennis events
        """
        self.__class__.tennis_category_id = self.ob_config.backend.ti.tennis.category_id
        if tests.settings.backend_env == 'prod':
            event1 = self.get_active_events_for_category(category_id=self.tennis_category_id)[0]
            self._logger.info(f'*** Found event: {event1}')
        else:
            self.check_sport_configured(self.tennis_category_id)
            self.ob_config.add_tennis_event_to_davis_cup()
            self.ob_config.add_tennis_event_to_european_open()
            self.ob_config.add_tennis_event_to_nice_open()

            start_time = self.get_date_time_formatted_string(hours=6)

            event_params = self.ob_config.add_tennis_event_to_autotest_trophy(
                start_time=self.get_date_time_formatted_string(hours=1))
            self.__class__.expected_events_order.append(f'{event_params.team1} v {event_params.team2}')

            event_params2 = self.ob_config.add_tennis_event_to_autotest_trophy(
                start_time=self.get_date_time_formatted_string(hours=2))
            self.__class__.expected_events_order.append(f'{event_params2.team1} v {event_params2.team2}')

            event_params3 = self.ob_config.add_tennis_event_to_autotest_trophy(
                start_time=self.get_date_time_formatted_string(hours=3))
            self.__class__.expected_events_order.append(f'{event_params3.team1} v {event_params3.team2}')

            event_params4 = self.ob_config.add_tennis_event_to_autotest_trophy(
                start_time=self.get_date_time_formatted_string(hours=4))
            self.__class__.expected_events_order.append(f'{event_params4.team1} v {event_params4.team2}')

            if self.device_type == 'desktop':
                tomorrow = self.get_date_time_formatted_string(days=1)
                self.ob_config.add_tennis_event_to_autotest_trophy(start_time=tomorrow)

                future = self.get_date_time_formatted_string(days=7)
                self.ob_config.add_tennis_event_to_autotest_trophy(start_time=future)

            for outright in range(0, 4):
                outright_name = f'Outright {int(time.time())}'
                self.ob_config.add_tennis_outright_event_to_autotest_league(
                    event_name=outright_name, start_time=start_time)
        self.__class__.start_date = f'{get_date_time_as_string(days=-1)}T21:00:00.000Z'
        query = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, str(self.tennis_category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      self.start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN,
                                      f'{get_date_time_as_string(days=2)}T21:00:00.000Z')) \
            .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME, OPERATORS.INTERSECTS, 'HH, MH, WH')) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME,
                                                                  OPERATORS.INTERSECTS, 'HH, MH, WH'))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN,
                                      self.start_date_minus))
        class_ids = self.get_class_ids_for_category(category_id=self.tennis_category_id)

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.tennis_category_id)
        events_list = ss_req.ss_event_to_outcome_for_class(query_builder=query, class_id=class_ids)
        self.verify_events_are_present(resp=events_list)

        sorted_leagues = self.sort_by_disp_order(events_list)
        self.__class__.league_name = sorted_leagues[0]
        self.__class__.expected_leagues_order = [item.upper() for item in sorted_leagues]

        self.__class__.expected_events_order = self.get_order_of_events(league=self.league_name,
                                                                        sports_list=events_list)

        suspend_date = f'{get_date_time_as_string(time_format="%Y-%m-%dT%H:%M:%S")}'
        outright_events_filter = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, str(self.tennis_category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_SORT_CODE, OPERATORS.INTERSECTS,
                                      vec.siteserve.OUTRIGHT_EVENT_SORT_CODES)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, suspend_date))

        outright_list = ss_req.ss_event_to_outcome_for_class(query_builder=outright_events_filter,
                                                             class_id=class_ids)
        self.verify_events_are_present(resp=outright_list)
        sorted_outright_leagues = self.sort_by_disp_order(outright_list)
        self.__class__.outright_league_name = sorted_outright_leagues[0]
        self.__class__.outright_events_order = self.get_order_of_events(league=self.outright_league_name,
                                                                        sports_list=outright_list)

        if self.device_type == 'desktop':
            tomorrow_end_date = f'{get_date_time_as_string(days=1)}T22:00:00.000Z'
            tomorrow_start_date = f'{get_date_time_as_string(days=0)}T22:00:00.000Z'

            tomorrow_events_filter = self.ss_query_builder \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, str(self.tennis_category_id))) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME,
                                                                      OPERATORS.INTERSECTS, 'HH'))) \
                .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, tomorrow_end_date)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                          tomorrow_start_date))

            future_start_date = f'{get_date_time_as_string(days=2)}T22:00:00.000Z'
            suspend_date = f'{get_date_time_as_string(time_format="%Y-%m-%dT%H:%M:%S")}'
            future_events_filter = self.ss_query_builder \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, str(self.tennis_category_id))) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME,
                                                                      OPERATORS.INTERSECTS, 'HH'))) \
                .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                          future_start_date)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                          suspend_date))

            tomorrow_events_list = ss_req.ss_event_to_outcome_for_class(query_builder=tomorrow_events_filter,
                                                                        class_id=class_ids)
            self.verify_events_are_present(resp=tomorrow_events_list)
            sorted_tomorrow_leagues = self.sort_by_disp_order(tomorrow_events_list)
            self.__class__.tomorrow_league_name = sorted_tomorrow_leagues[0].upper()
            self.__class__.tomorrow_events_order = self.get_order_of_events(league=self.tomorrow_league_name,
                                                                            sports_list=tomorrow_events_list)

            future_sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=future_events_filter,
                                                                      class_id=class_ids)
            self.verify_events_are_present(resp=future_sports_list)
            sorted_future_leagues = self.sort_by_disp_order(tomorrow_events_list)
            self.__class__.future_league_name = sorted_future_leagues[0].upper()
            self.__class__.future_events_order = self.get_order_of_events(league=self.future_league_name,
                                                                          sports_list=future_sports_list)

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_tap_tennis_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Tennis' icon on the Sports Menu Ribbon
        EXPECTED: *   Tennis Landing Page is opened
        EXPECTED: *   '**Matches**'->'**Today**' tab is opened by default (for desktop) / '**Matches** tab is opened by default (for mobile)
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        self.site.open_sport(self.get_sport_title(category_id=self.tennis_category_id))

        current_tab = self.site.tennis.tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.matches,
                         msg=f'\nDefault tab: "{current_tab}" opened'
                             f'\nExpected tab: "{self.expected_sport_tabs.matches}" opened')

        if self.device_type == 'desktop':
            current_date_tab = self.site.tennis.date_tab.current
            self.assertEqual(current_date_tab, vec.sb.SPORT_DAY_TABS.today,
                             msg=f'\nDefault tab: "{current_tab}" opened'
                                 f'\nExpected tab: "{self.expected_sport_tabs.matches}" opened')

        self.verify_section_collapse_expand()

    def test_003_verify_section_headers_titles(self):
        """
        DESCRIPTION: Verify section header's titles
        EXPECTED: The section header titles are in the following format and corresponds to the attributes:
        EXPECTED: **Category Name** + "** -** " + **Type Name**
        """
        self.verify_section_header_titles(outrights=True)

    def test_004_verify_competitions_sections_order(self):
        """
        DESCRIPTION: Verify Competitions sections order
        EXPECTED: Competitions sections are ordered by:
        EXPECTED: **Type displayOrder **in ascending order
        """
        sections = self.site.tennis.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg=f'No sections found')

        actual_order = list(map(lambda section: section.replace("\nSEE ALL", ""), list(sections.keys())))
        self.softAssert(self.assertListEqual, actual_order, self.expected_leagues_order,
                        msg=f'\nActual leagues order: "{actual_order}" '
                        f'\nExpected leagues order: "{self.expected_leagues_order}"')

    def test_005_verify_events_order(self, expected_events_order=None):
        """
        DESCRIPTION: Verify events order
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1.  **(rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true)) **(for 'Today' tab only, for desktop)
        EXPECTED: 2.  **startTime **- chronological order in the first instance
        EXPECTED: 3.  **Event displayOrder ** in ascending
        EXPECTED: 4.  **Alphabetical order**
        """
        all_sections = self.site.tennis.tab_content.accordions_list.items_as_ordered_dict
        sections = {}
        for section in all_sections:
            if ('SEE ALL' in section):
                x = section.split('\n')[0]
                sections[x] = all_sections[section]
            else:
                sections[section] = all_sections[section]

        self.assertTrue(sections, msg=f'No sections found')

        self.__class__.section_name = self.league_name.upper()
        self.__class__.autotest_section = sections.get(self.section_name)
        self.assertTrue(self.autotest_section, msg=f'Section "{self.section_name}" not found in "{sections.keys()}"')

        if not self.autotest_section.is_expanded():
            self.autotest_section.expand()
        self.assertTrue(self.autotest_section.is_expanded(), msg=f'Section "{self.section_name}" is not expanded')

        actual_events_order = list(self.autotest_section.items_as_ordered_dict)
        self.assertTrue(actual_events_order, msg=f'No events found')

        if expected_events_order is None:
            expected_events_order = self.expected_events_order
        self.softAssert(self.assertListEqual, actual_events_order, expected_events_order,
                        msg=f'\nActual events order: "{actual_events_order}" '
                        f'\nExpected events order: "{expected_events_order}"')

        self.autotest_section.collapse()

    def test_006_verify_displaying_of_team_names_within_the_events(self):
        """
        DESCRIPTION: Verify displaying of team names within the events
        EXPECTED: Team names are shown in the following format:
        EXPECTED: Team1_name Team2_name
        EXPECTED: (2 lines of text), where Team1_name is the name of Away team, and Team2_name is the name of Home team
        """
        self.verify_event_section()

    def test_007_tap_matches_tomorrow_tab_for_desktop_only(self):
        """
        DESCRIPTION: Tap 'Matches'->'Tomorrow' tab (for desktop only)
        EXPECTED: *   '**Tomorrow**' tab is opened
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        if self.device_type == 'desktop':
            self.site.tennis.date_tab.tomorrow.click()

            current_tab = self.site.tennis.date_tab.current_date_tab
            self.assertEqual(current_tab, vec.sb.SPORT_DAY_TABS.tomorrow,
                             msg=f'\nActual tab opened: "{current_tab}"'
                                 f'\nExpected tab opened: "{vec.sb.SPORT_DAY_TABS.tomorrow}"')

            self.__class__.max_number_of_sections = 1
            self.verify_section_collapse_expand()

    def test_008_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps №5-6
        EXPECTED: The same as on the steps №5-6
        """
        if self.device_type == 'desktop':
            self.section_name = self.tomorrow_league_name
            self.test_005_verify_events_order(expected_events_order=self.tomorrow_events_order)
            self.test_006_verify_displaying_of_team_names_within_the_events()

    def test_009_tap_matches_future_tab_for_desktop_only(self):
        """
        DESCRIPTION: Tap 'Matches'->'Future' tab (for desktop only)
        EXPECTED: *   '**Future**' tab is opened
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        if 'desktop' == self.device_type:
            self.site.tennis.date_tab.future.click()

            current_tab = self.site.tennis.date_tab.current_date_tab
            self.assertEqual(current_tab, vec.sb.SPORT_DAY_TABS.future,
                             msg=f'\nActual tab opened: "{current_tab}"'
                                 f'\nExpected tab opened: "{vec.sb.SPORT_DAY_TABS.future}"')

            self.__class__.max_number_of_sections = 1
            self.verify_section_collapse_expand()

    def test_010_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps №5-6
        EXPECTED: The same as on the steps steps №5-6
        """
        if self.device_type == 'desktop':
            self.test_005_verify_events_order(expected_events_order=self.future_events_order)
            self.test_006_verify_displaying_of_team_names_within_the_events()

    def test_011_tap_outrights_tab(self):
        """
        DESCRIPTION: Tap 'Outrights' tab
        EXPECTED: *   '**Outrights**' tab is opened
        EXPECTED: *   **All **sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by tapping the section's header
        """
        outrights_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights, self.tennis_category_id)

        result = self.site.tennis.tabs_menu.click_button(button_name=outrights_tab)
        self.assertTrue(result, msg=f'"{outrights_tab}" is not opened')

        current_tab = self.site.tennis.tabs_menu.current
        self.assertEqual(current_tab, outrights_tab,
                         msg=f'\nActual tab opened: "{current_tab}"'
                             f'\nExpected tab opened: "{outrights_tab}"')

        self.__class__.sections = self.site.tennis.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found')

        for section_name, section in list(self.sections.items()):
            section.scroll_to()
            self.assertFalse(section.is_expanded(expected_result=False), msg=f'Section "{section_name}" is expanded')
            section.expand()
            self.assertTrue(section.is_expanded(), msg=f'Section "{section_name}" is not expanded')

    def test_012_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps №5-6
        EXPECTED: The same as on the steps №5-6
        """
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.section_name = self.outright_league_name
        else:
            self.section_name = self.outright_league_name.upper()

        section = self.sections.get(self.section_name)
        self.assertTrue(section, msg=f'"{self.section_name}" section not found in "{self.sections.keys()}"')

        actual_events_order = list(map(lambda section: section.replace("\nSEE ALL", ""), list(section.items_as_ordered_dict.keys())))
        self.assertTrue(actual_events_order, msg=f'No events found in')

        self.assertListEqual(actual_events_order, self.outright_events_order,
                             msg=f'\nActual events order: "{actual_events_order}" '
                                 f'\nExpected events order: "{self.outright_events_order}"')
