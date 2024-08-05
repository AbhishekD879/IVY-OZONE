import time
from datetime import datetime

import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests
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
@pytest.mark.american_football
@pytest.mark.ob_smoke
@pytest.mark.cms
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.slow
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-53035')
@vtest
class Test_C28698_American_Football_Verify_Landing_pages(BaseSportTest):
    """
    TR_ID: C28698
    NAME: Verify American Football Landing pages
    DESCRIPTION: This test case verifies Landing pages
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   [BMA-15231: Changes to behaviour and display of US Sport events][1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-15231
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID (American Football=1)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: Current supported version of OB release can be found in the request by the list of events (Dev tools -> Network -> request URL in the "Headers" section of the request by the list of events)
    """
    keep_browser_open = True
    expected_events_order = []
    outright_events_order = []
    tomorrow_events_order = []
    future_events_order = []

    def verify_events_are_present(self, resp):
        event = next((event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')), None)
        if not event:
            raise SiteServeException(
                f'No active events found for category id "{self.ob_config.american_football_config.category_id}"')

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by DisplayOrder otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        sport_categories = {f"{sport['event']['categoryName']} - {sport['event']['typeName']}":
                            int(sport['event']['typeDisplayOrder']) for sport in sports_list}
        return sorted(sport_categories, key=lambda k: (sport_categories[k], k))

    def get_event_start_time(self, league: str, sports_list: list) -> dict:
        """
        Gets events start times
        :param sports_list: list of all sports
        :param league: str league name
        :return: return dictionary where key is name and value is event startTime
        """
        events = [event['event'] for event in sports_list if event['event']['typeName'].upper() in league.upper()]
        return {x['name']: x['startTime'] for x in events}

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
        DESCRIPTION: Create American Football events in OpenBet
        """
        category_id = self.ob_config.american_football_config.category_id
        self.__class__.sport_name = self.get_sport_title(category_id)

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=category_id)
        class_ids = self.get_class_ids_for_category(category_id=category_id)

        start_date = f'{get_date_time_as_string(days=0)}T00:00:00.000Z'
        end_date = f'{get_date_time_as_string(days=0)}T22:00:00.000Z' if self.device_type == 'desktop' \
            else f'{get_date_time_as_string(days=2)}T22:00:00.000Z'

        events_filter = self.ss_query_builder\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, str(category_id)))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME,
                                                                  OPERATORS.INTERSECTS, 'HH'))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, start_date))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, end_date))

        suspend_date = f'{get_date_time_as_string(time_format="%Y-%m-%dT%H:%M:%S")}'
        outright_events_filter = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, str(category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_SORT_CODE, OPERATORS.INTERSECTS,
                                      vec.siteserve.OUTRIGHT_EVENT_SORT_CODES)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, suspend_date))

        if tests.settings.backend_env == 'prod':
            event1 = self.get_active_events_for_category(category_id=category_id, expected_template_market='Money Line')[0]
            self._logger.info(f'*** Found event: {event1}')
        else:
            self.check_sport_configured(category_id)
            self.ob_config.add_american_football_event_to_ncaa_bowls()
            self.ob_config.add_american_football_event_to_nfl()
            self.ob_config.add_american_football_event_to_cfl()
            self.ob_config.add_american_football_event_to_autotest_league()

            start_time = self.get_date_time_formatted_string(hours=6)

            for i in range(0, 2):
                self.ob_config.add_american_football_event_to_autotest_league(start_time=start_time)

            for outright in range(0, 2):
                outright_name = f'Outright {int(time.time())}'
                self.ob_config.add_american_football_outright_event_to_autotest_league(event_name=outright_name,
                                                                                       start_time=start_time)

            if self.device_type == 'desktop':
                tomorrow = self.get_date_time_formatted_string(days=1)
                self.ob_config.add_american_football_event_to_autotest_league(start_time=tomorrow)

                future = self.get_date_time_formatted_string(days=7)
                self.ob_config.add_american_football_event_to_autotest_league(start_time=future)

        query = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, str(category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      self.start_date)) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME,
                                                                  OPERATORS.INTERSECTS, 'HH'))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN,
                                      self.start_date_minus))

        sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=query,
                                                           class_id=class_ids)
        sorted_leagues = self.sort_by_disp_order(sports_list)
        self.__class__.league_name = sorted_leagues[0]
        self.__class__.expected_leagues_order_upper = [item.upper() for item in sorted_leagues]

        events_list = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter,
                                                           class_id=class_ids)
        self.verify_events_are_present(resp=events_list)

        self.__class__.expected_events_order = self.get_order_of_events(league=self.league_name,
                                                                        sports_list=events_list)

        outright_list = ss_req.ss_event_to_outcome_for_class(query_builder=outright_events_filter,
                                                             class_id=class_ids)
        self.verify_events_are_present(resp=outright_list)
        self.__class__.outright_events_order = self.get_order_of_events(league=self.league_name,
                                                                        sports_list=outright_list)

        if self.device_type == 'desktop':
            tomorrow_end_date = f'{get_date_time_as_string(days=1)}T22:00:00.000Z'
            tomorrow_start_date = f'{get_date_time_as_string(days=0)}T22:00:00.000Z'

            tomorrow_events_filter = self.ss_query_builder \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, str(category_id))) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME,
                                                                      OPERATORS.INTERSECTS, 'HH'))) \
                .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, tomorrow_end_date)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, tomorrow_start_date))

            future_start_date = f'{get_date_time_as_string(days=2)}T22:00:00.000Z'
            suspend_date = f'{get_date_time_as_string(time_format="%Y-%m-%dT%H:%M:%S")}'
            future_events_filter = self.ss_query_builder \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, str(category_id))) \
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

    def test_002_tap_american_football_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'American Football' icon on the sports menu ribbon
        EXPECTED: *   American Football Landing Page is opened
        EXPECTED: *   **Matches** ->  **Today** tab is opened by default (for desktop)/ 'Matches' tab is opened (for mobile)
        EXPECTED: *   First **three** sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        self.site.open_sport(self.sport_name)
        current_tab = self.site.american_football.tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.matches,
                         msg=f'Default tab: "{current_tab}" opened '
                         f'is not as expected: "{self.expected_sport_tabs.matches}"')
        if self.device_type == 'desktop':
            current_date_tab = self.site.american_football.date_tab.current
            self.assertEqual(current_date_tab, vec.sb.SPORT_DAY_TABS.today,
                             msg=f'Default tab: "{current_tab}" opened '
                             f'is not as expected: "{self.expected_sport_tabs.matches}"')
        self.__class__.max_number_of_sections = 4
        self.verify_section_collapse_expand()

    def test_003_verify_section_headers_titles(self):
        """
        DESCRIPTION: Verify section header's titles
        EXPECTED: The section header titles are in the following format and corresponds to the attributes:
        EXPECTED: **categoryName** + **-** + **typeName**
        """
        self.verify_section_header_titles(outrights=True)

    def test_004_verify_competitions_sections_order(self):
        """
        DESCRIPTION: Verify Competitions sections order
        EXPECTED: Competitions sections are ordered by:
        EXPECTED: **Type displayOrder **in ascending order
        """
        sections = self.site.american_football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')

        section_name = self.expected_leagues_order_upper[0]
        self._logger.info(f'*** Section name is "{section_name}"')
        self.__class__.expected_section = sections.get(section_name)
        self.assertTrue(self.expected_section, msg=f'Section "{section_name}" not found')
        self.expected_section.expand()
        actual_leagues_order = list(sections.keys())
        self.softAssert(self.assertListEqual, actual_leagues_order, self.expected_leagues_order_upper,
                        msg=f'Actual displayed leagues order:\n"{actual_leagues_order}"\n '
                        f'is not as expected: \n"{self.expected_leagues_order_upper}"')  # BMA-48403

    def test_005_verify_events_order_in_the_competitions_section(self):
        """
        DESCRIPTION: Verify events order in the Competitions section
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1.  **(rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true)) **(for 'Today' tab only for desktop)
        EXPECTED: 2.  **startTime **- chronological order in the first instance
        EXPECTED: 3.  **Event displayOrder ** in ascending
        EXPECTED: 4.  **Alphabetical order**
        """
        actual_events_order = list(self.expected_section.items_as_ordered_dict)
        self.softAssert(self.assertListEqual, actual_events_order, self.expected_events_order,
                        msg=f'\nActual events order: \n"{actual_events_order}" '
                        f'\nis not as expected: \n"{self.expected_events_order}"')

    def test_006_verify_displaying_of_team_names_within_the_events(self):
        """
        DESCRIPTION: Verify displaying of team names within the events
        EXPECTED: Team names are shown in the following format:
        EXPECTED: Team1_name Team2_name
        EXPECTED: (2 lines of text), where Team1_name is the name of Away team, and Team2_name is the name of Home team
        """
        self.verify_event_section()

    def test_007_tap_tomorrow_tab_for_desktop_only(self):
        """
        DESCRIPTION: Tap **'Tomorrow'** tab (for desktop only)
        EXPECTED: *   '**Tomorrow**' tab is opened
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        if 'desktop' == self.device_type:
            self.site.american_football.date_tab.tomorrow.click()
            self.assertEqual(self.site.american_football.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.tomorrow,
                             msg=f'Current active date tab: "{self.site.american_football.date_tab.current_date_tab}", '
                             f'expected: "{vec.sb.SPORT_DAY_TABS.tomorrow}"')

            self.__class__.max_number_of_sections = 1
            self.verify_section_collapse_expand()

    def test_008_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps №5-6
        EXPECTED: The same as on the steps №5-6
        """
        if 'desktop' == self.device_type:
            self.__class__.sections = self.site.american_football.tab_content.accordions_list.items_as_ordered_dict
            section = self.sections.get(self.tomorrow_league_name)
            self.assertTrue(section,
                            msg=f'Section "{self.tomorrow_league_name}" is not found in "{self.sections.keys()}"')
            actual_events_order = list(section.items_as_ordered_dict.keys())
            self.softAssert(self.assertListEqual, actual_events_order, self.tomorrow_events_order,
                            msg=f'\nActual events order: \n"{actual_events_order}" '
                            f'\nis not as expected: \n"{self.tomorrow_events_order}"')
            self.verify_event_section()

    def test_009_tap_future_tab_for_desktop_only(self):
        """
        DESCRIPTION: Tap** 'Future'** tab (for desktop only)
        EXPECTED: *   '**Future**' tab is opened
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        if 'desktop' == self.device_type:
            self.site.american_football.date_tab.future.click()
            self.assertEqual(self.site.american_football.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.future,
                             msg=f'Current active date tab: "{self.site.american_football.date_tab.current_date_tab}", '
                             f'expected: "{vec.sb.SPORT_DAY_TABS.future}"')

            self.__class__.max_number_of_sections = 1
            self.verify_section_collapse_expand()

    def test_010_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps №5-6
        EXPECTED: The same as on the steps steps №5-6
        """
        if 'desktop' == self.device_type:
            self.__class__.sections = self.site.american_football.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(self.sections, msg='Can not find any section')
            section = self.sections.get(self.future_league_name)
            self.assertTrue(section,
                            msg=f'Section "{self.future_league_name}" is not found in "{self.sections.keys()}"')
            actual_events_order = list(section.items_as_ordered_dict.keys())
            self.softAssert(self.assertListEqual, actual_events_order, self.future_events_order,
                            msg=f'\nActual events order: \n"{actual_events_order}" '
                            f'\nis not as expected: \n"{self.future_events_order}"')
            self.verify_event_section()

    def test_011_tap_outrights_tab(self):
        """
        DESCRIPTION: Tap **'Outrights'** tab
        EXPECTED: *   '**Outrights**' tab is opened
        EXPECTED: *   **All **sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by tapping the section's header
        """
        result = self.site.american_football.tabs_menu.click_button(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights.upper())
        self.assertTrue(result, msg=f'"{self.expected_sport_tabs.outrights}" is not opened')

        current_tab = self.site.american_football.tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.outrights,
                         msg=f'Tab: "{current_tab}" opened '
                         f'is not as expected: "{self.expected_sport_tabs.outrights}"')

        self.__class__.sections = self.site.american_football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found')

        for section_name, section in list(self.sections.items()):
            section.scroll_to()
            self.assertFalse(section.is_expanded(expected_result=False, timeout=15), msg=f'Section "{section_name}" is expanded')
            section.expand()
            self.assertTrue(section.is_expanded(timeout=15), msg=f'Section "{section_name}" is not expanded')

    def test_012_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps №5-6
        EXPECTED: The same as on the steps №5-6
        """
        league = self.league_name \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else self.expected_leagues_order_upper[0]
        section = self.sections.get(league)
        self.assertTrue(section, msg=f'No section "{league}" found in sections "{self.sections}"')
        actual_events_order = list(section.items_as_ordered_dict.keys())
        self.assertListEqual(sorted(actual_events_order), sorted(self.outright_events_order),
                             msg=f'\nActual events order: \n"{sorted(actual_events_order)}" '
                             f'\nis not as expected: \n"{sorted(self.outright_events_order)}"')  # BMA-53035
