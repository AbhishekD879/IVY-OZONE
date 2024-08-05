from time import sleep
import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.adhoc_suite
@pytest.mark.sports_specific
@pytest.mark.football_specific
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C65949637_Verify_competitions_filtering_for_popular(BaseSportTest):
    """
    TR_ID: C65949637
    NAME: Verify competitions filtering for popular
    DESCRIPTION: This Testcase verifies competitions flitering for popular
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
        DESCRIPTION: Get events
        """
        if tests.settings.backend_env != 'prod':
            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
            if not competitions_countries:
                self.cms_config.get_system_configuration_item('CompetitionsFootball')
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
        EXPECTED: The Competitions tab should be loaded without any errors.
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
        cms_initial_class_ids = competitions_countries.get('InitialClassIDs', '')
        cms_initial_class_ids_ = cms_initial_class_ids.split(',')
        expected_initial_class_names = []

        for ss_class in response:
            for cms_initial_class in cms_initial_class_ids_:
                if ss_class['class']['id'] == cms_initial_class:
                    expected_initial_class_names.append(ss_class['class']['name'])

        class_ids = self.get_class_ids_for_category(category_id=self.ob_config.football_config.category_id)
        sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=query_builder,
                                                           class_id=class_ids)
        sorted_leagues = self.sort_by_disp_order(sports_list)
        self.__class__.expected_leagues_order_upper = [item.upper() if self.brand == 'bma' else item for item in
                                                       sorted_leagues]

        competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name, msg=f'"{competitions_tab_name}" tab is not active, '
                                                                f'active is "{active_tab}"')

        self.__class__.football = self.site.football.tab_content

        if self.is_mobile:
            initial_sections = self.football.competitions_categories.items_as_ordered_dict
            if cms_initial_class_ids:
                self.assertTrue(initial_sections,
                                msg=f'No Initial sections found on "{competitions_tab_name}" tab')
            else:
                self.assertFalse(initial_sections, msg=f'Initial sections found on "{competitions_tab_name}" tab')

            expected_initial_class_names = [name.upper().replace('FOOTBALL ', '') for name in
                                            expected_initial_class_names]
            expected_initial_class_names = list(set(expected_initial_class_names))
            self.assertListEqual(sorted(expected_initial_class_names), sorted(initial_sections),
                                 msg=f'Expected classes {sorted(expected_initial_class_names)} in initial part '
                                     f'are not the same as on ui {sorted(initial_sections)}')
        else:
            grouping_buttons = self.football.grouping_buttons
            expected_tab_name = vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME.upper() if self.brand == 'bma' else vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME
            self.assertEqual(grouping_buttons.current, expected_tab_name,
                             msg=f'"{expected_tab_name}" is not selected by default. '
                                 f'Default is "{grouping_buttons.current}"')
            if cms_initial_class_ids:
                initial_sections = self.football.accordions_list.items_as_ordered_dict
                first_accordian = list(initial_sections.values())[0]
                self.assertTrue(initial_sections,
                                msg=f'No Initial sections found on "{competitions_tab_name}" tab')
                self.assertTrue(first_accordian.is_expanded(),
                                msg='First accordian is not expanded by default')

            else:
                self.assertTrue(self.football.has_no_events_label(), msg='No events label is not shown')
                initial_sections = {}
            self.__class__.sections = self.football.accordions_list.items_as_ordered_dict
            self.assertTrue(self.sections, msg='Sections not found')

            self.assertTrue(grouping_buttons.items_as_ordered_dict, msg='No grouping buttons found')
            if self.brand == 'bma':
                self.assertListEqual(list(grouping_buttons.items_as_ordered_dict.keys()),
                                     [vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME.upper(),
                                      vec.sb_desktop.COMPETITIONS_SPORTS.upper()],
                                     msg=f'Grouping buttons are not the same as expected')
            else:
                self.assertListEqual(list(grouping_buttons.items_as_ordered_dict.keys()),
                                     [vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME,
                                      vec.sb_desktop.COMPETITIONS_SPORTS],
                                     msg=f'Grouping buttons are not the same as expected')

            if self.brand == 'bma':
                football_name_to_replace = 'FOOTBALL '
                expected_initial_class_names = [name.upper() for name in expected_initial_class_names]
            else:
                football_name_to_replace = 'Football '
            expected_initial_class_names = [name.replace(football_name_to_replace, '') for name in
                                            expected_initial_class_names]
            expected_initial_class_names = list(set(expected_initial_class_names))
            self.assertListEqual(sorted(expected_initial_class_names), sorted(initial_sections),
                                 msg=f'Expected classes {sorted(expected_initial_class_names)} in initial part '
                                     f'are not the same as on ui {sorted(initial_sections)}')

    def test_003_verify_popular_tab(self):
        """
        DESCRIPTION: Verify Popular tab
        EXPECTED: For Desktop:
        EXPECTED: The leagues (types) are displayed in Horizontal position with signposting if available.
        EXPECTED: For mobile/Tablet:
        EXPECTED: The leagues (types) are displayed in the list view
        """
        # Covered in step2

    def test_004_click_on_any_league_type_and_verify_competition_details_page(self):
        """
        DESCRIPTION: Click on any League type and verify Competition details page
        EXPECTED: For Desktop:
        EXPECTED: There are 'Matches and 'Outrights' tabs
        EXPECTED: 'Matches' tab is selected by default
        EXPECTED: 'Results' and 'League Table' widgets are displayed if available
        EXPECTED: Matches Result and Change competition are displayed
        EXPECTED: For mobile/Tablet:
        EXPECTED: Events from the relevant league (type) are displayed
        EXPECTED: There are 3 tabs (navigation buttons) on the page: 'Matches', 'Results', 'Outrights', standings
        EXPECTED: 'Matches' tab is selected by default
        EXPECTED: Matches Result and Change competition are displayed
        """
        if self.device_type == 'desktop':
            # self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[vec.sb_desktop.COMPETITIONS_SPORTS].click()
            competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        else:
            competitions = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
        self.assertTrue(competitions, msg='No competitions are present on page')

        if tests.settings.backend_env == 'prod':
            competition_league = vec.siteserve.PREMIER_LEAGUE_NAME
            if tests.settings.brand == 'ladbrokes' and self.device_type == 'desktop':
                league = vec.siteserve.ENGLAND.title()
            else:
                league = vec.siteserve.ENGLAND
        else:
            if tests.settings.brand == 'ladbrokes' and self.device_type == 'desktop':
                league = 'Auto Test'
            else:
                league = 'AUTO TEST'
            competition_league = vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME
        competition = competitions[league]
        competition.expand()
        wait_for_haul(5)
        leagues = wait_for_result(lambda: competition.items_as_ordered_dict,
                                  name='Leagues list is loaded',
                                  timeout=10)
        self.assertTrue(leagues, msg='No leagues are present on page')
        self.assertIn(competition_league, leagues.keys(),
                      msg=f'League "{competition_league}" is not found in "{list(leagues.keys())}"')
        self.__class__.league = leagues[competition_league]
        self.league.click()
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

    def test_005_verify_market_switcher_on_matches_tab(self):
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
        market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper() if self.brand == 'ladbrokes' and \
                                                                                                             self.device_type == 'desktop' else vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default
        options = self.site.football.tab_content.dropdown_market_selector
        self.assertEqual(options.selected_market_selector_item.upper(),
                         market_selector_default_value.upper(),
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: {options.selected_market_selector_item.upper()}\n'
                             f'Expected: {market_selector_default_value.upper()}')
        markets_dropdown_list = list(options.items_as_ordered_dict.keys())
        for market in markets_dropdown_list:
            options.select_value(value=market)
            sleep(2)
            options = self.site.football.tab_content.dropdown_market_selector

    def test_006_verify_change_competition_dropdown(self):
        """
        DESCRIPTION: Verify change competition dropdown
        EXPECTED: Desktop and mobile:
        EXPECTED: change competition dropdown should be displayed and when selected on specfic competition it should be displayed.
        """
        self.site.competition_league.title_section.competition_selector_link.click()
        if self.device_type == 'desktop':
            countries = self.site.competition_league.competitions_selector.items_as_ordered_dict
        else:
            countries= self.site.competition_league.competition_list.items_as_ordered_dict
        self.assertTrue(countries, msg="list of countries are not displayed")
        for section_name, section in countries.items():
            section.click()
            if self.device_type == 'desktop':
                leagues = section.league_selector.items_as_ordered_dict
            else:
                leagues = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(leagues, msg='No leagues found in Leagues selector')
            break
        self.site.competition_league.title_section.competition_selector_link.click()

    def test_007_verify_signpostings_and_favourite_icons(self):
        """
        DESCRIPTION: Verify Signpostings and Favourite icons
        EXPECTED: Sign postings (build your bet, price boost etc)
        EXPECTED: Favourite (star) icon should be displayed
        """
        # covered in C28596
