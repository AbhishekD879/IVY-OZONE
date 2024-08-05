import time
import pytest
import tests
import voltron.environments.constants as vec
from faker import Faker
from datetime import datetime
from tests.base_test import vtest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.cms
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.motorbikes
@pytest.mark.frequent_blocker
@vtest
class Test_C28728_Verify_Motor_Bikes_Landing_pages(BaseSportTest):
    """
    TR_ID: C28728
    NAME: Verify Motor Bikes Landing pages
    DESCRIPTION: This test case verifies Landing pages
    DESCRIPTION: Story related: BMA-2280 Create a Motor Bikes sport within the Application
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID (Motor Bikes=23)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)expected_events_order_new
    """
    keep_browser_open = True
    expected_events_order = []

    def verify_events_are_present(self, resp):
        event = next((event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')), None)
        if not event:
            raise SiteServeException(
                f'No active events found for category id "{self.ob_config.backend.ti.motor_bikes.category_id}"')

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by typeDisplayOrder otherwise sort by name
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
        event_start_times = self.get_event_start_time(league=league, sports_list=sports_list)

        event_start_times_converted = []
        for name, start_time in event_start_times.items():
            date_time_obj = datetime.strptime(start_time.split(',')[0], self.ob_format_pattern)
            event_start_times_converted.append((name, date_time_obj.timetuple()))

        expected_order_tuple = sorted(event_start_times_converted, key=lambda x: (x[1], x[0]))
        return [x for x, _ in expected_order_tuple]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Motor Bikes events in OpenBet
        """
        self.__class__.motor_bikes_category_id = self.ob_config.backend.ti.motor_bikes.category_id
        self.__class__.sport_name = self.get_sport_title(self.motor_bikes_category_id)
        if tests.settings.backend_env == 'prod':
            event1 = self.get_active_events_for_category(category_id=self.motor_bikes_category_id)[0]
            self._logger.info(f'*** Found event: {event1}')
        else:
            self.check_sport_configured(self.motor_bikes_category_id)
            f = Faker()
            start_time = self.get_date_time_formatted_string(hours=6)
            event_name1 = f'Auto race {f.city()}'
            self.ob_config.add_motor_bikes_world_superbikes_championship_outright_event(event_name=event_name1)

            event_name2 = f'Auto race {f.city()}'
            self.ob_config.add_motor_bikes_world_superbikes_philip_island_outright_event(event_name=event_name2)

            event_name3 = f'Auto race {f.city()}'
            self.ob_config.add_motor_bikes_world_superbikesbrno_gp_outright_event(event_name=event_name3)

            for outright in range(0, 4):
                outright_name = f'Outright {int(time.time())}'
                self.ob_config.add_motor_bikes_event(event_name=outright_name, start_time=start_time)

        suspend_date = f'{get_date_time_as_string(time_format="%Y-%m-%dT%H:%M:%S")}'
        query = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, str(self.motor_bikes_category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, suspend_date))
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.motor_bikes_category_id)
        class_ids = self.get_class_ids_for_category(category_id=self.motor_bikes_category_id)
        sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=query,
                                                           class_id=class_ids)
        self.verify_events_are_present(resp=sports_list)
        self.__class__.expected_order = [item.upper() for item in self.sort_by_disp_order(sports_list)]
        self.__class__.league_name = self.expected_order[0]

        events_list = ss_req.ss_event_to_outcome_for_class(query_builder=query,
                                                           class_id=class_ids)

        self.__class__.expected_events_order = self.get_order_of_events(league=self.league_name,
                                                                        sports_list=events_list)

        outright_events_filter = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, str(self.motor_bikes_category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_SORT_CODE, OPERATORS.INTERSECTS,
                                      vec.siteserve.OUTRIGHT_EVENT_SORT_CODES)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, suspend_date))

        outright_list = ss_req.ss_event_to_outcome_for_class(query_builder=outright_events_filter,
                                                             class_id=class_ids)
        self.verify_events_are_present(resp=outright_list)
        sorted_outright_leagues = self.sort_by_disp_order(outright_list)
        self.__class__.outright_league_name = sorted_outright_leagues[0]
        self.__class__.expected_outright_events_order = self.get_order_of_events(league=self.outright_league_name,
                                                                                 sports_list=outright_list)

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_tap_motor_bikes_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Motor Bikes' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop:**
        EXPECTED: *   Motor Bikes Landing Page is opened
        EXPECTED: *   '**Events**' tab is opened by default
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: **Mobile:**
        EXPECTED: * Motor Bikes Landing Page (single view) is opened
        EXPECTED: * All available events for this sport are displayed on 1 page
        EXPECTED: * Available modules (in-play/upcoming) and sections (outrights/specials) are displayed one below another
        """
        self.site.open_sport(self.sport_name)
        expected_sport_tabs = [self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions, self.motor_bikes_category_id),
                               self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights, self.motor_bikes_category_id)]

        current_tab = self.site.motor_bikes.tabs_menu.current
        if self.device_type == 'mobile':
            self.assertIn(current_tab, expected_sport_tabs,
                          msg=f'Default tab: "{current_tab}" opened is not as expected: "{expected_sport_tabs}"')
        else:
            # For coral default tab is Matches
            expected_default_tab = self.expected_sport_tabs.matches if self.brand != 'ladbrokes' else self.expected_sport_tabs.events
            self.assertEqual(current_tab, expected_default_tab,
                             msg=f'Default tab: "{current_tab}" opened '
                             f'is not as expected: "{expected_default_tab}"')

        self.__class__.max_number_of_sections = 4
        if self.brand != 'ladbrokes':
            self.verify_section_collapse_expand()

    def test_003_verify_section_headers_titles(self):
        """
        DESCRIPTION: Verify section header's titles
        EXPECTED: The section header titles are in the following format and correponds to the attributes:
        EXPECTED: **categoryName** + "** -** " + **typeName**
        """
        self.verify_section_header_titles(outrights=True)

    def test_004_verify_competitions_sections_order(self):
        """
        DESCRIPTION: Verify Competitions sections order
        EXPECTED: Competitions sections are ordered by:
        EXPECTED: **Type displayOrder **in ascending order
        """
        result = self.site.motor_bikes.tabs_menu.click_button(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper())
        self.assertTrue(result, msg=f'"{self.expected_sport_tabs.competitions}" is not opened')
        sections = self.site.motor_bikes.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        actual_order = list(sections.keys())
        self.assertListEqual(actual_order, self.expected_order,
                             msg=f'Actual displayed leagues order:\n"{actual_order}"\n '
                             f'is not as expected: \n"{self.expected_order}"')

    def test_005_verify_events_order_in_the_competitions_section(self, outrights=False):
        """
        DESCRIPTION: Verify events order in the Competitions section
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1.  **(rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true)) **(for 'Today' tab only for Desktop)
        EXPECTED: 2.  **startTime **- chronological order in the first instance
        EXPECTED: 3.  **Event displayOrder ** in ascending
        EXPECTED: 4.  **Alphabetical order**
        """
        available_events_order = self.expected_outright_events_order if outrights else self.expected_events_order
        sections = self.site.motor_bikes.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        if self.brand != 'ladbrokes':
            league = self.league_name.upper()
        else:
            league = self.league_name
        self.__class__.autotest_section = sections.get(league)
        self.assertTrue(self.autotest_section,
                        msg=f'Section "{league}" not found in "{sections.keys()}"')
        self.autotest_section.expand()
        actual_events_order = list(self.autotest_section.items_as_ordered_dict)
        expected_events_order = []
        for event in available_events_order:
            if event in actual_events_order:
                expected_events_order.append(event)
        self.assertListEqual(actual_events_order, expected_events_order,
                             msg=f'\nActual events order: \n"{actual_events_order}" '
                                 f'\nis not as expected: \n"{expected_events_order}"')
        self.autotest_section.collapse()

    def test_006_tap_outrights_section(self):
        """
        DESCRIPTION: Tap 'Outrights' section
        DESCRIPTION: Note: for Mobile view Outright events are displayed in Outrights section (if available)
        EXPECTED: *  Available '**Outrights**' are displayed
        EXPECTED: *   **All **sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by tapping the section's header
        """
        result = self.site.motor_bikes.tabs_menu.click_button(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights.upper())
        self.assertTrue(result, msg=f'"{self.expected_sport_tabs.outrights}" is not opened')
        current_tab = self.site.motor_bikes.tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.outrights,
                         msg=f'Tab: "{current_tab}" opened is not as expected:"{self.expected_sport_tabs.outrights}"')
        self.__class__.sections = self.site.motor_bikes.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found')

        for section_name, section in list(self.sections.items()):
            self.assertFalse(section.is_expanded(expected_result=False), msg=f'Section "{section_name}" is expanded')
            section.expand()
            self.assertTrue(section.is_expanded(timeout=10), msg=f'Section "{section_name}" is not expanded')

    def test_007_repeat_steps_5(self):
        """
        DESCRIPTION: Repeat step №5
        EXPECTED: The same as on the step №5
        """
        if self.device_type == 'desktop':
            self.league_name = self.outright_league_name
        else:
            self.league_name = self.outright_league_name.upper()
        self.test_005_verify_events_order_in_the_competitions_section(outrights=True)
