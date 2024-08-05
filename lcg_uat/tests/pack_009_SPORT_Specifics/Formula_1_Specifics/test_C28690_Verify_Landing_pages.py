from datetime import datetime

import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from faker import Faker

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.formula1
@pytest.mark.frequent_blocker
@vtest
class Test_C28690_Verify_Formula_1_Landing_pages(BaseSportTest):
    """
    TR_ID: C28690
    NAME: Verify Formula 1 Landing pages
    DESCRIPTION: This test case verifies Landing pages
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID (Formula 1=24)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    available_events_order = []
    tomorrow_events_order = []
    outright_events_order = []
    future_events_order = []

    def verify_events_are_present(self, resp):
        event = next((event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')), None)
        if not event:
            raise SiteServeException(
                f'No active events found for category id "{self.ob_config.backend.ti.formula_1.category_id}"')

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by DisplayOrder otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        order = 'displayOrder' if self.brand == 'bma' else 'typeDisplayOrder'
        sport_categories = {f"{sport['event']['categoryName']} - {sport['event']['typeName']}": int(sport['event'][f'{order}']) for sport in sports_list}
        return sorted(sport_categories, key=lambda k: (sport_categories[k], k))

    def get_event_start_time(self, league: str, sports_list: list) -> dict:
        """
        Gets events start times
        :param sports_list: list of all sports
        :param league: str league name
        :return: return dictionary where key is name and value is event startTime
        """
        events = []
        for event in sports_list:
            if event['event']['typeName'] in league:
                events.append(event['event'])

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
        DESCRIPTION: Create Formula 1 event
        """
        category_id = self.ob_config.backend.ti.formula_1.category_id
        self.__class__.sport_name = self.get_sport_title(category_id)

        start_date = f'{get_date_time_as_string(days=0)}T00:00:00.000Z'
        end_date = f'{get_date_time_as_string(days=0)}T22:00:00.000Z'
        todays_events_filter = self.ss_query_builder\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, str(category_id)))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, start_date))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, end_date))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE))

        if tests.settings.backend_env == 'prod':
            event1 = self.get_active_events_for_category(category_id=category_id, expected_template_market='Outright')[0]
            self._logger.info(f'*** Found today\'s event: {event1}')

        else:
            self.check_sport_configured(category_id)
            faker = Faker()
            start_time = self.get_date_time_formatted_string(hours=6)
            self.ob_config.add_formula_1_european_grand_prix_outright_event()
            self.ob_config.add_formula_1_indian_grand_prix_outright_event()
            self.ob_config.add_formula_1_united_states_grand_prix_outright_event()

            event1 = f'Outright Formula 1 Event {faker.city()}'
            self.ob_config.add_formula_1_british_grand_prix_outright_event(event_name=event1, start_time=start_time)

            event2 = f'Outright Formula 1 Event {faker.city()}'
            self.ob_config.add_formula_1_british_grand_prix_outright_event(event_name=event2, start_time=start_time)

            event3 = f'Outright Formula 1 Event {faker.city()}'
            self.ob_config.add_formula_1_british_grand_prix_outright_event(event_name=event3, start_time=start_time)

            event4 = f'Outright Formula 1 Event {faker.city()}'
            self.ob_config.add_formula_1_british_grand_prix_outright_event(event_name=event4, start_time=start_time)

            if self.device_type == 'desktop':
                tomorrow = self.get_date_time_formatted_string(days=1)
                event5 = f'Outright Formula 1 Event {faker.city()}'
                self.ob_config.add_formula_1_british_grand_prix_outright_event(start_time=tomorrow, event_name=event5)

                future = self.get_date_time_formatted_string(days=7)
                event6 = f'Outright Formula 1 Event {faker.city()}'
                self.ob_config.add_formula_1_united_states_grand_prix_outright_event(start_time=future, event_name=event6)

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=category_id)

        class_ids = self.get_class_ids_for_category(category_id=category_id)

        sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=todays_events_filter,
                                                           class_id=class_ids)

        self.__class__.expected_leagues_order = [item.upper() for item in self.sort_by_disp_order(sports_list)]

        self.__class__.league = self.expected_leagues_order[0]

        self.__class__.available_events_order = self.get_order_of_events(league=self.league.title(), sports_list=sports_list)

        if self.device_type == 'desktop':

            tomorrow_end_date = f'{get_date_time_as_string(days=1)}T22:00:00.000Z'

            tomorrow_events_filter = self.ss_query_builder \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, str(category_id)))\
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M'))\
                .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, end_date))\
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, tomorrow_end_date))

            future_start_date = f'{get_date_time_as_string(days=2)}T22:00:00.000Z'
            suspend_date = f'{get_date_time_as_string(time_format="%Y-%m-%dT%H:%M:%S")}'
            future_events_filter = self.ss_query_builder\
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, str(category_id)))\
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
                .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE))\
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, future_start_date))\
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, suspend_date))

            outright_events_filter = self.ss_query_builder \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, str(category_id))) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_SORT_CODE, OPERATORS.INTERSECTS,
                                          vec.siteserve.OUTRIGHT_EVENT_SORT_CODES)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, suspend_date))

            tomorrow_sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=tomorrow_events_filter,
                                                                        class_id=class_ids)
            self.verify_events_are_present(resp=tomorrow_sports_list)
            self.__class__.tomorrow_events_order = self.get_order_of_events(league=tomorrow_sports_list[0]['event']['typeName'],
                                                                            sports_list=tomorrow_sports_list)

            future_sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=future_events_filter,
                                                                      class_id=class_ids)
            self.verify_events_are_present(resp=future_sports_list)
            self.__class__.future_events_order = self.get_order_of_events(league=future_sports_list[0]['event']['typeName'],
                                                                          sports_list=future_sports_list)
            self.__class__.future_type_name = f'{self.sport_name.title()} - {future_sports_list[0]["event"]["typeName"]}'.upper()

            outright_sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=outright_events_filter,
                                                                        class_id=class_ids)
            self.verify_events_are_present(resp=outright_sports_list)
            self.__class__.outright_type_name = f'{self.sport_name.title()} - {outright_sports_list[0]["event"]["typeName"]}'
            self.__class__.outright_events_order = self.get_order_of_events(league=self.outright_type_name,
                                                                            sports_list=outright_sports_list)

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_tap_formula_1_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Formula 1' icon on the Sports Menu Ribbon
        EXPECTED: Desktop:
        EXPECTED: * Formula 1 Landing Page is opened
        EXPECTED: * '**Events**' tab is opened by default
        EXPECTED: * First **three **sections are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: Mobile:
        EXPECTED: * Formula 1 Landing Page (single view) is opened
        EXPECTED: * All available events for this sport are displayed on 1 page
        EXPECTED: * Available modules (in-play/upcoming) and sections (outrights/specials) are displayed one below another
        """
        self.site.open_sport(self.sport_name)
        self.site.wait_content_state(state_name=self.sport_name)
        if self.device_type == 'mobile':
            formula_content = self.site.formula_1.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(formula_content, msg='Formula 1 section not found')
        else:
            current_tab = self.site.formula_1.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.events,
                             msg=f'Default tab: "{current_tab}" opened '
                             f'is not as expected: "{self.expected_sport_tabs.events}"')
        self.__class__.max_number_of_sections = 4

    def test_003_verify_section_headers_titles(self):
        """
        DESCRIPTION: Verify section header's titles
        EXPECTED: The section header titles are in the following format and corresponds to the attributes:
        EXPECTED: **categoryName** + "** -** " + **typeName**
        """
        self.verify_section_header_titles(outrights=True)

    def test_004_verify_by_races_sections_order(self):
        """
        DESCRIPTION: Verify 'By Races sections order
        EXPECTED: Races sections are ordered by:
        EXPECTED: **Type displayOrder **in ascending order
        """
        self.__class__.sections = self.site.formula_1.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found')
        actual_leagues_order = list(self.sections.keys())
        self.assertListEqual(actual_leagues_order, self.expected_leagues_order,
                             msg=f'Actual displayed leagues order:\n"{actual_leagues_order}"\n '
                                 f'is not as expected: \n"{self.expected_leagues_order}"')

    def test_005_verify_events_order_in_the_by_races_section(self):
        """
        DESCRIPTION: Verify events order in the 'By Races' section
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1.  **(rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true)) **(for 'Today' tab only)
        EXPECTED: 2.  **startTime **- chronological order in the first instance
        EXPECTED: 3.  **Event displayOrder ** in ascending
        EXPECTED: 4.  **Alphabetical order**
        """
        autotest_section = self.sections.get(self.league)
        self.assertTrue(autotest_section, msg=f'No "{self.league}" section found in "{self.sections.keys()}"')
        autotest_section.expand()
        actual_events_order = list(autotest_section.items_as_ordered_dict)
        expected_events_order = []
        for event in self.available_events_order:
            if event in actual_events_order:
                expected_events_order.append(event)
        self.softAssert(self.assertListEqual, actual_events_order, expected_events_order,
                        msg=f'\nActual events order: \n"{actual_events_order}" '
                        f'\nis not as expected: \n"{expected_events_order}"')

    def test_006_tap_tomorrow_tab_for_desktop_only(self):
        """
        DESCRIPTION: Tap 'Tomorrow' tab (for desktop only)
        EXPECTED: *   '**Tomorrow**' tab is opened
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by tapping the section's header
        """
        if self.device_type == 'desktop':
            self.site.formula_1.date_tab.tomorrow.click()
            self.assertEqual(self.site.formula_1.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.tomorrow,
                             msg=f'Current active date tab: "{self.site.formula_1.date_tab.current_date_tab}", '
                             f'expected: "{vec.sb.SPORT_DAY_TABS.tomorrow}"')
            self.__class__.max_number_of_sections = 1
            self.verify_section_collapse_expand()

    def test_007_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: The same as on the steps №4-5
        """
        if self.device_type == 'desktop':
            self.__class__.sections = self.site.formula_1.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(self.sections, msg='No sections are found')
            section_name = tests.settings.formula_1_british_grand_prix
            section = self.sections.get(section_name, None)
            self.assertTrue(section, msg=f'No "{section_name}" section found in "{self.sections.keys()}"')
            actual_events_order = list(section.items_as_ordered_dict.keys())
            self.softAssert(self.assertListEqual, actual_events_order, self.tomorrow_events_order,
                            msg=f'\nActual events order: \n"{actual_events_order}" '
                            f'\nis not as expected: \n"{self.tomorrow_events_order}"')

    def test_008_tap_future_tab_for_desktop_only(self):
        """
        DESCRIPTION: Tap 'Future' tab (for desktop only)
        EXPECTED: *   '**Future**' tab is opened
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by tapping the section's header
        """
        if self.device_type == 'desktop':
            self.site.formula_1.date_tab.future.click()
            self.assertEqual(self.site.formula_1.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.future,
                             msg=f'Current active date tab: "{self.site.formula_1.date_tab.current_date_tab}", '
                             f'expected: "{vec.sb.SPORT_DAY_TABS.future}"')
            self.__class__.max_number_of_sections = 1
            self.verify_section_collapse_expand()

    def test_009_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: The same as on the steps steps №4-5
        """
        if self.device_type == 'desktop':
            self.__class__.sections = self.site.formula_1.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(self.sections, msg='No sections are found')
            section = self.sections.get(self.future_type_name)
            self.assertTrue(section, msg=f'No "{self.future_type_name}" section found in "{self.sections.keys()}"')
            actual_events_order = list(section.items_as_ordered_dict.keys())
            self.softAssert(self.assertListEqual, actual_events_order, self.future_events_order,
                            msg=f'\nActual events order: \n"{actual_events_order}" '
                            f'\nis not as expected: \n"{self.future_events_order}"')

    def test_010_tap_outrights_tab_for_desktop_onlynote_outrights_for_mobile_are_in_separate_section_on_single_view_page(self):
        """
        DESCRIPTION: Tap 'Outrights' tab (for desktop only)
        DESCRIPTION: Note: Outrights for mobile are in separate section on single view page.
        EXPECTED: *   '**Outrights**' tab is opened
        EXPECTED: *   **All **sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by tapping the section's header
        """
        if self.device_type == 'desktop':
            result = self.site.formula_1.tabs_menu.click_button(button_name=self.expected_sport_tabs.outrights)
            self.assertTrue(result, msg=f'"{self.expected_sport_tabs.outrights}" is not opened')
            current_tab = self.site.formula_1.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.outrights,
                             msg=f'Default tab: "{current_tab}" opened '
                             f'is not as expected: "{self.expected_sport_tabs.outrights}"')
            self.__class__.sections = self.site.formula_1.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(self.sections, msg='No sections found')
            for section_name, section in list(self.sections.items()):
                self.assertFalse(section.is_expanded(expected_result=False),
                                 msg=f'Section "{section_name}" is expanded')
                section.expand()
                self.assertTrue(section.is_expanded(timeout=10), msg=f'Section "{section_name}" is not expanded')

    def test_011_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: The same as on the steps №4-5
        """
        if self.device_type == 'desktop':
            if self.brand != 'ladbrokes':
                outright_type = self.outright_type_name.upper()
            else:
                outright_type = self.outright_type_name
            section = self.sections.get(outright_type)
            self.assertTrue(section,
                            msg=f'No "{outright_type}" section found in "{self.sections.keys()}"')
            actual_events_order = list(section.items_as_ordered_dict.keys())
            self.assertListEqual(actual_events_order, self.outright_events_order,
                                 msg=f'\nActual events order: \n"{actual_events_order}" '
                                 f'\nis not as expected: \n"{self.outright_events_order}"')
