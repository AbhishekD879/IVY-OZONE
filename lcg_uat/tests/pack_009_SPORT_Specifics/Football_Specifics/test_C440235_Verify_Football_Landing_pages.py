import pytest
import time
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can not create event in Prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.sports
@pytest.mark.outrights
@vtest
class Test_C440235_Verify_Football_Landing_pages(BaseSportTest):
    """
    TR_ID: C440235
    NAME: Verify Football Landing pages
    DESCRIPTION: This test case verifies Football Landing pages
    PRECONDITIONS: Preconditions
    PRECONDITIONS: 1) In order to get a list with Regions (Classes IDs) and Leagues (Types IDs) use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: XX - sports Category ID (Football=16)
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID (Football=16)
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
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
            f"{sport['event']['className'].replace('football ', '')} - {sport['event']['typeName']}": (
                int(sport['event']['typeDisplayOrder']),
                int(sport['event']['classDisplayOrder']))
            for sport in sports_list
        }
        return sorted(sport_categories, key=lambda k: (sport_categories[k][0], sport_categories[k][1], k))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Football events in OpenBet
        """
        self.__class__.football_category_id = self.ob_config.backend.ti.football.category_id
        self.check_sport_configured(self.football_category_id)
        self.__class__.section_name = tests.settings.football_autotest_league
        start_time = self.get_date_time_formatted_string(hours=6)
        self.ob_config.add_football_event_to_spanish_la_liga()
        self.ob_config.add_football_event_to_england_premier_league()
        self.ob_config.add_football_event_to_autotest_league2()

        event_params = self.ob_config.add_autotest_premier_league_football_event(
            start_time=self.get_date_time_formatted_string(hours=1))
        self.__class__.expected_events_order.append(f'{event_params.team1} v {event_params.team2}')

        event_params2 = self.ob_config.add_autotest_premier_league_football_event(
            start_time=self.get_date_time_formatted_string(hours=2))
        self.__class__.expected_events_order.append(f'{event_params2.team1} v {event_params2.team2}')

        event_params3 = self.ob_config.add_autotest_premier_league_football_event(
            start_time=self.get_date_time_formatted_string(hours=3))
        self.__class__.expected_events_order.append(f'{event_params3.team1} v {event_params3.team2}')

        event_params4 = self.ob_config.add_autotest_premier_league_football_event(
            start_time=self.get_date_time_formatted_string(hours=4))
        self.__class__.expected_events_order.append(f'{event_params4.team1} v {event_params4.team2}')

        for outright in range(0, 4):
            self.__class__.outright_name = f'Outright {int(time.time())}'
            self.ob_config.add_autotest_premier_league_football_outright_event(event_name=self.outright_name,
                                                                               start_time=start_time)
            self.__class__.outright_events_order.append(self.outright_name)

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.football_category_id)
        query = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                      str(self.football_category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, self.end_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      self.start_date_minus))

        class_ids = self.get_class_ids_for_category(category_id=self.football_category_id)
        sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=query,
                                                           class_id=class_ids)

        self.__class__.expected_leagues_order = [item.upper() for item in self.sort_by_disp_order(sports_list)]

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage', timeout=30)

    def test_002_tap_football_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: * 'Matches'  page is opened by default
        EXPECTED: * First three sections are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by clicking the section's header
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football', timeout=20)
        matches_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                              self.football_category_id)
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, matches_tab,
                         msg=f'Default tab: "{current_tab}" opened '
                             f'is not as expected: "{matches_tab}"')

        self.__class__.max_number_of_sections = 3
        self.verify_section_collapse_expand()

    def test_003_verify_section_headers_titles(self):
        """
        DESCRIPTION: Verify section header's titles
        EXPECTED: * The section header titles are in the following format and correponds to the attributes:
        EXPECTED: * className (sport name is not displayed) + "" - "" + typeName
        """
        self.verify_section_header_titles(outrights=True)

    def test_004_verify_leagues_sections_order(self):
        """
        DESCRIPTION: Verify Leagues sections order
        EXPECTED: Leagues sections are ordered by:
        EXPECTED: * Class displayOrder in ascending order where minus ordinals are displayed first
        EXPECTED: * Type displayOrder in ascending order
        """
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        actual_leagues_order_ui = list(sections.keys())
        actual_leagues_order = []
        for i in range(len(actual_leagues_order_ui)):
            actual_leagues_order.append('FOOTBALL ' + actual_leagues_order_ui[i])
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
        EXPECTED: * (rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true)) (for 'Today' tab only for Desktop)
        EXPECTED: * startTime - chronological order in the first instance
        EXPECTED: * Event displayOrder  in ascending
        EXPECTED: * Alphabetical order
        """
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        autotest_section = sections.get(self.section_name)
        self.assertTrue(autotest_section, msg=f'Section "{self.section_name}" not found')
        actual_events_order = autotest_section.items_as_ordered_dict
        self.assertTrue(actual_events_order, msg='No events found')
        actual_events_order_filtered = [x for x in list(actual_events_order.keys()) if x in self.expected_events_order]
        for event in actual_events_order_filtered:
            self.assertIn(event, self.expected_events_order,
                          msg=f'Actual displayed events order:\n"{event}"\n '
                              f'is not as expected: \n"{self.expected_events_order}"')

    def test_006_go_to_outrights_events_page(self):
        """
        DESCRIPTION: Go to 'Outrights' Events page
        EXPECTED: * 'Outrights' Events page is opened
        EXPECTED: * All sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by tapping the section's header
        """
        outrights_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights,
                                                self.football_category_id)
        result = self.site.football.tabs_menu.click_button(button_name=outrights_tab)
        self.assertTrue(result, msg=f'"{outrights_tab}" is not opened')

        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, outrights_tab,
                         msg=f'Default tab: "{current_tab}" opened is not as expected: "{outrights_tab}"')

        self.__class__.sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found')

        for section_name, section in list(self.sections.items()):
            section.scroll_to()
            self.assertFalse(section.is_expanded(expected_result=False, timeout=3),
                             msg=f'Section "{section_name}" is expanded')
            section.expand()
            self.assertTrue(section.is_expanded(timeout=3), msg=f'Section "{section_name}" is not expanded')

    def test_007_repeat_steps_3_5(self):
        """
        DESCRIPTION: Repeat steps №3-5
        EXPECTED: The same as on the steps №3-5
        """
        league_name = tests.settings.football_autotest_league.title() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else tests.settings.football_autotest_league
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
