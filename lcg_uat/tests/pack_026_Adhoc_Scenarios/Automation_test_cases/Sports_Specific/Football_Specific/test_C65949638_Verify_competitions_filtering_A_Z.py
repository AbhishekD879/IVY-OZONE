from time import sleep

import pytest
from crlat_siteserve_client.utils.date_time import get_date_time_as_string

import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.adhoc_suite
@pytest.mark.sports_specific
@pytest.mark.football_specific
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C65949638_Verify_competitions_filtering_A_Z(BaseSportTest):
    """
    TR_ID: C65949638
    NAME: Verify competitions filtering  A-Z
    DESCRIPTION: This test case verifies Verify competitions filtering  A-Z
    PRECONDITIONS: 1. Make sure that 'COMPETITIONS' tab is enabled in cms.
    """
    keep_browser_open = True

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by DisplayOrder otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        sport_categories = {f"{sport['event']['className']} - {sport['event']['typeName']}":
                                int(sport['event']['typeDisplayOrder']) for sport in sports_list}
        return sorted(sport_categories, key=lambda k: (sport_categories[k], k))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event and league
        """
        if tests.settings.backend_env != 'prod':
            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsFootball')
            if str(self.ob_config.football_config.autotest_class.class_id) not in competitions_countries.get(
                    'A-ZClassIDs').split(','):
                raise CmsClientException(f'{tests.settings.football_autotest_competition} class '
                                         f'is not configured on Competitions tab')

            self.ob_config.add_autotest_premier_league_football_event(selections_number=1)
            self.ob_config.add_autotest_premier_league_football_outright_event(ew_terms=self.ew_terms)
            self.__class__.section_name_list = 'Auto Test' if self.brand == 'ladbrokes' else tests.settings.football_autotest_competition
            self.__class__.league = tests.settings.football_autotest_competition_league.title()
        else:
            event = self.get_competition_with_results_and_standings_tabs(
                category_id=self.ob_config.football_config.category_id, raise_exceptions=True)
            sport_name = event.class_name.upper().split(" ")
            if sport_name[0] == vec.siteserve.FOOTBALL_TAB.upper():
                self.__class__.section_name_list = sport_name[1]
            else:
                self.__class__.section_name_list = sport_name[0]
            self.__class__.league = event.league_name
        self.__class__.is_mobile = self.device_type == 'mobile'

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the Lads/Coral application
        EXPECTED: Application should be launched successfully
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')

    def test_002_navigate_to_football_landing_page_and_verify_competitions_tab(self):
        """
        DESCRIPTION: Navigate to football Landing Page and verify Competitions tab
        EXPECTED: The Compettions tab should be loaded without any errors.
        EXPECTED: Desktop:
        EXPECTED: 'Popular' and 'A-Z' switchers should be displayed below Sports Sub Tabs
        EXPECTED: 'Popular' switcher should be selected by default and highlighted
        EXPECTED: Mobile:
        EXPECTED: Country Competitions should be displayed
        EXPECTED: 'A-Z' Competitions  should be displayed
        EXPECTED: All accordions are collapsed by default
        EXPECTED: 'A-Z'Competitions are ordered alphabetically
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.football_config.category_id)
        query_builder = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                      self.ob_config.football_config.category_id)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.HAS_OPEN_EVENT))
        response = ss_req.ss_class(class_id='', query_builder=query_builder)
        competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
        if not competitions_countries:
            competitions_countries = self.get_system_configuration_item('CompetitionsFootball')
        cms_az_class_ids = competitions_countries['A-ZClassIDs'].split(',')
        expected_az_class_names = []

        for ss_class in response:
            for cms_az_class in cms_az_class_ids:
                if ss_class['class']['id'] == cms_az_class:
                    expected_az_class_names.append(ss_class['class']['name'])

        class_ids = self.get_class_ids_for_category(category_id=self.ob_config.football_config.category_id)

        end_date = f'{get_date_time_as_string(days=1)}T00:00:00.000Z'
        start_date = f'{get_date_time_as_string(days=0)}T00:00:00.000Z'
        query_builder = self.ss_query_builder \
            .add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, end_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      self.start_date_minus)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                      self.ob_config.football_config.category_id)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.HAS_OPEN_EVENT))
        sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=query_builder,
                                                           class_id=class_ids)
        sorted_leagues = self.sort_by_disp_order(sports_list)
        self.__class__.expected_leagues_order_upper = [item.upper() if self.brand == 'bma' else item for item in
                                                       sorted_leagues]
        # *************** Verifying Competitions tab **************
        competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name, msg=f'"{competitions_tab_name}" tab is not active, '
                                                                f'active is "{active_tab}"')

        self.__class__.football = self.site.football.tab_content

        if self.is_mobile:
            a_z_competition_name = self.football.a_z_competition_label.name
            self.assertTrue(a_z_competition_name,
                            msg=f'A-Z competition name label is not found on "{competitions_tab_name}" tab')
            self.__class__.initial_sections = self.football.all_competitions_categories.items_as_ordered_dict
            self.assertTrue(self.initial_sections, msg=f'No A-Z sections found on "{competitions_tab_name}" tab')

            if cms_az_class_ids:
                self.assertTrue(self.initial_sections,
                                msg=f'No Initial sections found on "{competitions_tab_name}" tab')
            else:
                self.assertFalse(self.initial_sections, msg=f'Initial sections found on "{competitions_tab_name}" tab')

            expected_az_class_names = [name.upper().replace('FOOTBALL ', '') for name in expected_az_class_names]

            expected_az_class_names = list(set(expected_az_class_names))

            self.assertListEqual(sorted(expected_az_class_names), sorted(self.initial_sections),
                                 msg=f'Expected classes {sorted(expected_az_class_names)} in A-Z part '
                                     f'are not the same as on ui {sorted(self.initial_sections)}')

        else:
            self.site.football.tab_content.grouping_buttons.click_item(vec.sb_desktop.COMPETITIONS_SPORTS)
            self.__class__.countries_sections = self.football.accordions_list.items_as_ordered_dict
            if cms_az_class_ids:
                first_accordian = list(self.countries_sections.values())[0]
                self.assertTrue(self.countries_sections,
                                msg=f'No Initial sections found on "{competitions_tab_name}" tab')
                self.assertTrue(first_accordian.is_expanded(),
                                msg='First accordian is not expanded by default')

            else:
                self.assertTrue(self.football.has_no_events_label(), msg='No events label is not shown')

            if self.brand == 'bma':
                football_name_to_replace = 'FOOTBALL '
                expected_az_class_names = [name.upper() for name in expected_az_class_names]
            else:
                football_name_to_replace = 'Football '

            expected_az_class_names = [name.replace(football_name_to_replace, '') for name in expected_az_class_names]

            expected_az_class_names = list(set(expected_az_class_names))

            self.assertListEqual(sorted(expected_az_class_names), sorted(self.countries_sections),
                                 msg=f'Expected classes {sorted(expected_az_class_names)} in A-Z part '
                                     f'are not the same as on ui {sorted(self.countries_sections)}')

    def test_003_verify_a_z_tab(self):
        """
        DESCRIPTION: Verify A-Z Tab
        EXPECTED: For Desktop:
        EXPECTED: List of Country competitions will display and by default first country league will be in expanded mode.
        EXPECTED: For mobile/Tablet:
        EXPECTED: List of Country Competitions will be displayed and in collapse mode.
        """
        # covered in step2

    def test_004_click_on_any_country_competition(self):
        """
        DESCRIPTION: Click on any country competition
        EXPECTED: Should be in expanded mode when clicked on Country competition.
        """
        # covered in step5

    def test_005_click_on_any_league_type_and_verify_competition_details_page(self):
        """
        DESCRIPTION: Click on any League type and verify Competition details page
        EXPECTED: For Desktop:
        EXPECTED: 'Matches' tab is selected by default
        EXPECTED: List of events will be displayed under Matches tab
        EXPECTED: Matches Result and Change competition are displayed
        EXPECTED: Time filters are displayed
        EXPECTED: For mobile/Tablet:
        EXPECTED: Events from the relevant league (type) are displayed under Matches tab.
        EXPECTED: 'Matches' tab is selected by default
        EXPECTED: Matches Result and Change competition are displayed
        """
        if self.device_type == 'desktop':
            sections = self.countries_sections
        else:
            sections = self.initial_sections
        self.assertTrue(sections, msg='No competitions are present on page')
        if self.section_name_list.title() not in sections:
            if self.device_type == 'desktop':
                grouping_buttons = self.site.football.tab_content.grouping_buttons.items_as_ordered_dict
                self.assertTrue(grouping_buttons, msg='No grouping buttons found')
                grouping_buttons[vec.sb_desktop.COMPETITIONS_SPORTS].click()
                sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            else:
                sections = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
            self.assertTrue(sections, msg='No countries found')
        if self.section_name_list not in ['USA', 'UEFA Club Competitions']:
            if self.device_type == 'desktop':
                section_name = self.section_name_list if self.brand == 'bma' else self.section_name_list.title()
            else:
                section_name = self.section_name_list if self.brand == 'bma' else self.section_name_list.title().upper()
        else:
            section_name = self.section_name_list
        section = sections.get(section_name)
        self.assertTrue(section, msg=f'Section with name "{section_name}" is not found in "{sections.keys()}"')
        section.expand()
        leagues = wait_for_result(lambda: section.get_items(name=self.league),
                                  name=f'"{self.section_name_list}" to expand for "{self.league}"', timeout=3)
        self.assertTrue(leagues, msg=f'No events are present for the league "{self.league}"')
        league = leagues.get(self.league)
        self.assertTrue(league, msg=f'Cannot find "{self.league}" on Competitions page')
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

        self.__class__.tabs_menu = self.site.competition_league.tabs_menu
        self.assertTrue(self.tabs_menu, msg='Tabs menu was not found')

        if self.is_mobile:
            for tab_name, tab in self.tabs_menu.items_as_ordered_dict.items():
                self.assertIn(tab_name, vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values(),
                              msg=f'Market switcher tab {tab_name} is not present in the list')

            current_tab = self.tabs_menu.current
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}"')
        else:
            desktop_tabs = list(vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()) \
                if self.brand == 'bma' else [tab.title() for tab in
                                             vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()]
            for tab_name, tab in self.tabs_menu.items_as_ordered_dict.items():
                self.assertIn(tab_name, desktop_tabs,
                              msg=f'Market switcher tab {tab_name} is not present in the list')
            self.site.wait_content_state_changed()
            current_tab = self.tabs_menu.current
            expected_tab = vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches if self.brand == 'bma' else vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches.capitalize()
            self.assertEqual(current_tab, expected_tab,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{desktop_tabs[0]}"')
            try:
                self.__class__.results_widget = self.site.competition_league.results_widget
                self.assertTrue(self.results_widget.is_displayed(), msg='Results widget is not displayed')
            except Exception:
                self._logger.info(f'The result widget is not displayed')

    def test_006_verify_market_switcher_on_matches_tab(self):
        """
        DESCRIPTION: Verify market switcher on matches tab
        EXPECTED: Desktop:
        EXPECTED: Match result market switcher should be selected as default
        EXPECTED: Market switcher dropdown should be displayed and when clicked on specfic market it should be displayed.
        EXPECTED: Mobile:
        EXPECTED: Match result market switcher should be selected as default
        EXPECTED: Market switcher dropdown should be displayed and when clicked on specfic market it should be displayed.
        """
        football_tab_content = self.site.football.tab_content
        self.assertTrue(football_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on Football landing page')
        market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()
        options = self.site.football.tab_content.dropdown_market_selector
        actual_default_market_name = options.selected_market_selector_item.upper()
        self.assertEqual(actual_default_market_name, market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: {actual_default_market_name}\n'
                             f'Expected: {market_selector_default_value}')
        markets_dropdown_list = list(options.items_as_ordered_dict.keys())
        for market in markets_dropdown_list:
            options.select_value(value=market)
            sleep(2)
            options = self.site.football.tab_content.dropdown_market_selector

    def test_007_verify_change_competition_dropdown(self):
        """
        DESCRIPTION: Verify change competition dropdown
        EXPECTED: Desktop and mobile:
        EXPECTED: change competition dropdown should be displayed and when selected on specfic competition it should be displayed.
        """
        self.site.competition_league.title_section.competition_selector_link.click()
        if self.device_type == 'desktop':
            countries = self.site.competition_league.competitions_selector.has_items
        else:
            countries = self.site.competition_league.a_z_competition_list.has_items
        self.assertTrue(countries, msg="list of countries are not displayed")
        section_name, section = self.site.competition_league.competitions_selector.first_item if self.device_type == 'desktop' else self.site.competition_league.a_z_competition_list.first_item
        section.click()
        leagues = section.league_selector.has_items if self.device_type == 'desktop' else self.site.contents.tab_content.accordions_list.has_items
        self.assertTrue(leagues, msg='No leagues found in Leagues selector')
        self.site.competition_league.title_section.competition_selector_link.click()
