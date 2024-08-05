import time

import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.basketball
@pytest.mark.slow
@pytest.mark.outrights
@pytest.mark.sports
@vtest
class Test_C28715_Verify_Basketball_Landing_pages(BaseSportTest):
    """
    TR_ID: C28715
    NAME: Verify Basketball Landing pages
    DESCRIPTION: This test case verifies Basketball Landing page
    DESCRIPTION: BMA-15231: Changes to behaviour and display of US Sport events
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID (Basketball=6)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE: **Current supported version of OB release can be found in the request by the list of events (Dev tools -> Network -> request URL in the "Headers" section of the request by the list of events)
    """
    keep_browser_open = True
    expected_events_order = []
    outright_events_order = []

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by classDisplayOrder otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        sport_categories = {
            f"{sport['event']['className'].replace('Basketball ', '')} - {sport['event']['typeName']}": (int(sport['event']['typeDisplayOrder']),
                                                                                                         int(sport['event']['classDisplayOrder']))
            for sport in sports_list
        }
        return sorted(sport_categories, key=lambda k: (sport_categories[k][0], sport_categories[k][1], k))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Basketball events in OpenBet
        """
        self.__class__.basketball_category_id = self.ob_config.backend.ti.basketball.category_id
        self.check_sport_configured(self.basketball_category_id)
        self.__class__.section_name = tests.settings.basketball_autotest_league
        start_time = self.get_date_time_formatted_string(hours=6)
        self.ob_config.add_basketball_event_to_croatian_league()
        self.ob_config.add_basketball_event_to_austrian_league()
        self.ob_config.add_basketball_event_to_us_league()

        event_params = self.ob_config.add_basketball_event_to_autotest_league(
            start_time=self.get_date_time_formatted_string(hours=1))
        self.__class__.expected_events_order.append(f'{event_params.team2} v {event_params.team1}')

        event_params2 = self.ob_config.add_basketball_event_to_autotest_league(
            start_time=self.get_date_time_formatted_string(hours=2))
        self.__class__.expected_events_order.append(f'{event_params2.team2} v {event_params2.team1}')

        event_params3 = self.ob_config.add_basketball_event_to_autotest_league(
            start_time=self.get_date_time_formatted_string(hours=3))
        self.__class__.expected_events_order.append(f'{event_params3.team2} v {event_params3.team1}')

        event_params4 = self.ob_config.add_basketball_event_to_autotest_league(
            start_time=self.get_date_time_formatted_string(hours=4))
        self.__class__.expected_events_order.append(f'{event_params4.team2} v {event_params4.team1}')

        for outright in range(0, 4):
            self.__class__.outright_name = f'Outright {int(time.time())}'
            self.ob_config.add_basketball_outright_event_to_autotest_league(event_name=self.outright_name,
                                                                            start_time=start_time)
            self.__class__.outright_events_order.append(self.outright_name)

        self.__class__.sport_name = self.get_sport_title(self.basketball_category_id)

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.basketball_category_id)
        query = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                      str(self.basketball_category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, self.end_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      self.start_date_minus))

        class_ids = self.get_class_ids_for_category(category_id=self.basketball_category_id)
        sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=query,
                                                           class_id=class_ids)

        self.__class__.expected_leagues_order = [item.upper() for item in self.sort_by_disp_order(sports_list)]

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: * Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_tap_basketball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Basketball' icon on the Sports Menu Ribbon
        EXPECTED: *   Basketball Landing Page is opened
        EXPECTED: *   '**Matches**' tab is opened by default
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        matches_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, self.basketball_category_id)
        current_tab = self.site.basketball.tabs_menu.current
        self.assertEqual(current_tab, matches_tab,
                         msg=f'Default tab: "{current_tab}" opened '
                         f'is not as expected: "{matches_tab}"')

        self.__class__.max_number_of_sections = 4
        self.verify_section_collapse_expand()

    def test_003_verify_accordions_headers_titles(self):
        """
        DESCRIPTION: Verify accordions header's titles
        EXPECTED: The section header titles are in the following format and corresponds to the attributes:
        EXPECTED: **className** (sport name is not displayed) + ""** -** "" + t**ypeName**
        """
        self.verify_section_header_titles(outrights=True)

    def test_004_verify_leagues_sections_order(self):
        """
        DESCRIPTION: Verify Leagues sections order
        EXPECTED: Leagues sections are ordered by:
        EXPECTED: 1. Class **displayOrder **in ascending order where minus ordinals are displayed first
        EXPECTED: 2. Type **displayOrder **in ascending order
        """
        sections = self.site.basketball.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        actual_leagues_order = list(sections.keys())
        for league in actual_leagues_order:
            self.assertIn(league, self.expected_leagues_order,
                          msg=f'Actual displayed leagues order:\n"{actual_leagues_order}"\n '
                              f'is not as expected: \n"{self.expected_leagues_order}"')
        autotest_section = sections.get(self.section_name)
        self.assertTrue(autotest_section, msg=f'Section "{self.section_name}" not found')
        autotest_section.expand()

    def test_005_verify_events_order_in_the_league_section(self):
        """
        DESCRIPTION: Verify events order in the League section
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1. **(rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true))**  (for 'Today' tab only)
        EXPECTED: 2. **startTime **- chronological order in the first instance
        EXPECTED: 3. **Event displayOrder ** in ascending
        EXPECTED: 4. **Alphabetical order**
        """
        sections = self.site.basketball.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        autotest_section = sections.get(self.section_name)
        self.assertTrue(autotest_section, msg=f'Section "{self.section_name}" not found')
        actual_events_order = autotest_section.items_as_ordered_dict
        self.assertTrue(actual_events_order, msg='No events found')
        # filters out existing events not created by script, but also preserves order of events
        actual_events_order_filtered = [x for x in list(actual_events_order.keys()) if x in self.expected_events_order]
        self.assertListEqual(actual_events_order_filtered, self.expected_events_order,
                             msg=f'\nActual events order: \n"{actual_events_order_filtered}" '
                             f'\nis not as expected: \n"{self.expected_events_order}"')

    def test_006_verify_displaying_of_team_names_within_the_events(self):
        """
        DESCRIPTION: Verify displaying of team names within the events
        EXPECTED: Team names are shown in the following format:
        EXPECTED: Team1_name Team2_name
        EXPECTED: (2 lines of text), where Team1_name is the name of Away team, and Team2_name is the name of Home team
        """
        self.verify_event_section()

    def test_007_tap_outrights_tab(self):
        """
        DESCRIPTION: Tap 'Outrights' tab
        EXPECTED: *   '**Outrights**' tab is opened
        EXPECTED: *   **All **sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by tapping the section's header
        """
        outrights_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights, self.basketball_category_id)

        result = self.site.basketball.tabs_menu.click_button(button_name=outrights_tab)
        self.assertTrue(result, msg=f'"{outrights_tab}" is not opened')

        current_tab = self.site.basketball.tabs_menu.current
        self.assertEqual(current_tab, outrights_tab,
                         msg=f'Default tab: "{current_tab}" opened is not as expected: "{outrights_tab}"')

        self.__class__.sections = self.site.basketball.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found')

        for section_name, section in list(self.sections.items()):
            section.scroll_to()
            self.assertFalse(section.is_expanded(expected_result=False, timeout=3), msg=f'Section "{section_name}" is expanded')
            section.expand()
            self.assertTrue(section.is_expanded(timeout=3), msg=f'Section "{section_name}" is not expanded')

    def test_008_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps №5-6
        EXPECTED: The same as on the steps №5-6
        """
        league_name = tests.settings.basketball_autotest_league.title() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else tests.settings.basketball_autotest_league
        section = self.sections.get(league_name)
        self.assertTrue(section, msg=f'Cannot found "{league_name}" among "{list(self.sections.keys())}"')
        actual_events_order = list(section.items_as_ordered_dict.keys())
        self.assertIn(self.outright_name, actual_events_order,
                      msg=f'Cannot find "{self.outright_name}" in "{actual_events_order}"')

        intersection = [x for x in actual_events_order if
                        x in self.outright_events_order]  # that's because there might be a lot more events than we create

        self.assertListEqual(intersection, self.outright_events_order,
                             msg=f'\nActual events order: \n"{intersection}" '
                             f'\nis not as expected: \n"{self.outright_events_order}"')
