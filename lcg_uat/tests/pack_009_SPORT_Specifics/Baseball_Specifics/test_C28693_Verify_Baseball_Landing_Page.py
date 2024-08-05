from datetime import datetime

import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from selenium.common.exceptions import StaleElementReferenceException

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.baseball
@pytest.mark.cms
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28693_Verify_Baseball_Landing_Page(BaseSportTest):
    """
    TR_ID: C28693
    NAME: Verify Baseball Landing pages
    DESCRIPTION: This test case verifies Landing pages
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   [BMA-15231: Changes to behaviour and display of US Sport events][1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-15231
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID (Baseball=5)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:** Current supported version of OB release can be found in the request by the list of events (Dev tools -> Network -> request URL in the "Headers" section of the request by the list of events)
    """
    keep_browser_open = True
    expected_events_order = []

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by typeDisplayOrder otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        sport_categories = {}
        for sport in sports_list:
            class_name = str(sport['event']['className'])
            category_name = str(sport['event']['categoryName'])
            if class_name == category_name:
                sport_name = class_name
            else:
                sport_name = class_name.replace(category_name, '', 1).strip().replace('All', '').strip()
            name = f"{sport_name} - {sport['event']['typeName']}"
            sport_categories[name] = sport['event']['typeDisplayOrder']
        return sorted(sport_categories, key=lambda k: (sport_categories[k], k))

    def get_event_start_time(self, league: str, sports_list: list) -> dict:
        """
        Gets events start times
        :param sports_list: list of all sports
        :param league: str league name
        :return: return dictionary where key is name and value is event startTime
        """
        events = [event['event'] for event in sports_list if event['event']['typeName'].upper() in league]
        return {x['name']: x['startTime'] for x in events}

    def get_order_of_events(self, league: str, sports_list: list) -> list:
        """
        Having response gets the expected order of events in coupon
        :param league: str league name
        :param sports_list: list of all sports
        :return: expected order of events in league
        """
        event_start_times_converted = []
        event_start_times = self.get_event_start_time(league=league, sports_list=sports_list)

        for name, start_time in event_start_times.items():
            date_time_obj = datetime.strptime(start_time.split(',')[0], self.ob_format_pattern)
            event_start_times_converted.append((name, date_time_obj.timetuple()))
        expected_order_tuple = sorted(event_start_times_converted, key=lambda x: (x[1], x[0]))

        return [x for x, _ in expected_order_tuple]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Baseball events in OpenBet
        """
        self.__class__.baseball_category_id = self.ob_config.backend.ti.baseball.category_id
        self.__class__.sport_name = self.get_sport_title(self.baseball_category_id)

        if tests.settings.backend_env == 'prod':
            event1 = self.get_active_events_for_category(category_id=self.baseball_category_id)[0]
            self._logger.info(f'*** Found event: {event1}')
        else:
            self.check_sport_configured(self.baseball_category_id)
            self.ob_config.add_baseball_event_to_us_league()
            self.ob_config.add_baseball_event_to_germany_league()
            self.ob_config.add_baseball_event_to_world_league()

            self.ob_config.add_baseball_event_to_autotest_league(start_time=self.get_date_time_formatted_string(hours=1))
            self.ob_config.add_baseball_event_to_autotest_league(start_time=self.get_date_time_formatted_string(hours=2))
            self.ob_config.add_baseball_event_to_autotest_league(start_time=self.get_date_time_formatted_string(hours=3))
            self.ob_config.add_baseball_event_to_autotest_league(start_time=self.get_date_time_formatted_string(hours=4))

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.baseball_category_id)

        query = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS,
                                      str(self.baseball_category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      self.start_date)) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME,
                                                                  OPERATORS.INTERSECTS, 'HH'))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN,
                                      self.start_date_minus))
        if tests.settings.backend_env != 'prod':
            query.add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.TEMPLATE_MARKET_NAME, OPERATORS.INTERSECTS,
                                           self.ob_config.baseball_config.baseball_autotest.autotest_league.market_name))
        class_ids = self.get_class_ids_for_category(category_id=self.baseball_category_id)
        sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=query,
                                                           class_id=class_ids)
        self.__class__.expected_leagues_order = [item.upper() for item in self.sort_by_disp_order(sports_list)]
        self.__class__.league_name = self.expected_leagues_order[0]
        self.__class__.expected_events_order = self.get_order_of_events(league=self.league_name, sports_list=sports_list)

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_tap_baseball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Baseball' icon on the Sports Menu Ribbon
        EXPECTED: Desktop:
        EXPECTED: * Baseball Landing Page is opened
        EXPECTED: * '**Events**' tab is opened by default
        EXPECTED: * First **three **sections are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: Mobile:
        EXPECTED: * Baseball Landing Page (single view) is opened
        EXPECTED: * All available events for this sport are displayed on 1 page
        EXPECTED: * Available modules (in-play/upcoming) and sections (outrights/specials) are dibassplayed one below another
        """
        self.navigate_to_page(name='sport/baseball')
        self.site.wait_content_state(state_name=self.sport_name)
        matches_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, self.baseball_category_id)
        current_tab = self.site.baseball.tabs_menu.current
        self.assertEqual(current_tab, matches_tab,
                         msg=f'Default tab: "{current_tab}" opened is not as expected: "{matches_tab}"')

        self.__class__.max_number_of_sections = 4
        self.verify_section_collapse_expand()

    def test_003_verify_accordions_headers_titles(self):
        """
        DESCRIPTION: Verify accordions header's titles
        EXPECTED: The section header titles are in the following format and corresponds to the attributes:
        EXPECTED: **className** (sport name is not displayed) + ""** -** "" + t**ypeName**
        """
        self.verify_section_header_titles(outrights=True)

    def test_004_verify_leagues_sections_order(self):
        """
        DESCRIPTION: Verify Leagues sections order
        EXPECTED: Leagues sections are ordered by:
        EXPECTED: 1.  Class **displayOrder **in ascending order where minus ordinals are displayed first
        EXPECTED: 2.  Type **displayOrder **in ascending order
        """
        self.__class__.sections = self.site.baseball.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found')
        actual_leagues_order = list(self.sections.keys())
        actual_leagues_order_list = []
        for i in actual_leagues_order:
            actual_leagues_order_list.append(i.split('\n')[0])
        for league in actual_leagues_order_list:
            self.assertIn(league, self.expected_leagues_order,
                          msg=f'Actual displayed league:\n"{actual_leagues_order}"\n '
                              f'cannot be found in: \n"{self.expected_leagues_order}"')

    def test_005_verify_events_order_in_the_league_section(self):
        """
        DESCRIPTION: Verify events order in the League section
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1.  **(rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true))** (for 'Today' tab only for desktop)
        EXPECTED: 2.  **startTime **- chronological order in the first instance
        EXPECTED: 3.  **Event displayOrder ** in ascending
        EXPECTED: 4.  **Alphabetical order**
        """
        autotest_section = self.sections.get(self.league_name)
        self.assertTrue(autotest_section, msg=f'Section "{self.league_name}" not found in "{self.sections.keys()}"')
        autotest_section.expand()
        try:
            actual_events_order = list(autotest_section.items_as_ordered_dict)
        except StaleElementReferenceException:
            sections = self.site.baseball.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found')
            autotest_section = sections.get(self.league_name)
            self.assertTrue(autotest_section, msg=f'Section "{self.league_name}" not found in "{sections.keys()}"')
            actual_events_order = list(autotest_section.items_as_ordered_dict)
        for league in actual_events_order:
            self.assertIn(league, actual_events_order,
                          msg=f'Actual event "{league}" cannot be found in "{actual_events_order}"')


    def test_006_verify_displaying_of_team_names_within_the_events(self):
        """
        DESCRIPTION: Verify displaying of team names within the events
        EXPECTED: Team names are shown in the following format:
        EXPECTED: Team1_name Team2_name
        EXPECTED: (2 lines of text), where Team1_name is the name of Away team, and Team2_name is the name of Home team
        """
        self.verify_event_section()