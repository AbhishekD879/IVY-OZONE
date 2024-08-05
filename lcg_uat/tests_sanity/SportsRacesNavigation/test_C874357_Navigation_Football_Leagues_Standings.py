import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2 # removed ts2, stg2 markers due to result/standing tabs will be displayed for real events
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.sanity
@vtest
class Test_C874357_Navigation_Football_Leagues_Standings(BaseSportTest):
    """
    TR_ID: C874357
    NAME: Navigation Football Leagues (Standings)
    DESCRIPTION: This test case verifies 'Leagues' page for Football sport
    PRECONDITIONS: [1] Link to check league table results: http://www.espnfc.com/english-league-championship/24/table
    """
    keep_browser_open = True
    table_headers = ['POS', '', 'P', 'W', 'D', 'L', 'GD', 'PTS']
    default_row_number = 5
    show_less_button_name = vec.big_competitions.SHOW_LESS.upper()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event and league
        """
        event = self.get_competition_with_results_and_standings_tabs(
            category_id=self.ob_config.football_config.category_id, raise_exceptions=True)
        sport_name = event.class_name.upper().split(" ")
        if sport_name[0] == vec.sb.FOOTBALL.upper():
            self.__class__.section_name_list = sport_name[1]
        else:
            self.__class__.section_name_list = sport_name[0]
        self.__class__.league = event.league_name

        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        self.__class__.league_table_label = vec.sb.LEAGUE_TABLE_LABEL.title() if self.brand == 'bma' else vec.sb.LEAGUE_TABLE_LABEL

    def test_001_tap_football_icon_from_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football 'icon from sports menu ribbon
        EXPECTED: Football sport page is opened
        """
        self.site.open_sport(name=self.get_sport_title(category_id=self.ob_config.football_config.category_id).upper())
        self.site.wait_content_state(state_name=vec.sb.FOOTBALL)

    def test_002_tap_competitions_tab_on_the_sport_page(self):
        """
        DESCRIPTION: Tap 'Competitions' Tab on the sport page
        EXPECTED: * List of available leagues is displayed
        EXPECTED: * First Competition (league) type is expanded, the rest are displayed collapsed
        """
        if self.is_mobile:
            self.site.football.tabs_menu.click_button(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper())
            active_tab = self.site.football.tabs_menu.current
            self.assertEqual(active_tab, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper(),
                             msg=f'"{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()}" tab is not active, '
                                 f'active is "{active_tab}"')

            country_sections = self.site.football.tab_content.competitions_categories.items_as_ordered_dict
            self.assertTrue(country_sections, msg='Competitions page does not have any section')
            section_name_1, section_1 = list(country_sections.items())[0]

            self.assertTrue(section_1.is_expanded(), msg=f'First league "{section_name_1}" is not expanded by default')

            for section_name, section in list(country_sections.items())[1:]:
                self.assertFalse(section.is_expanded(expected_result=False),
                                 msg=f'"{section_name}" league is expanded by default')

    def test_003_select_any_competition(self):
        """
        DESCRIPTION: Select any Competition
        EXPECTED: Competition page is opened with tabs available (some may be missing): matches, outrights, results,standings
        EXPECTED: List of events is displayed within selected Competition (League) in Matches tab
        """
        if self.is_mobile:
            sections = self.site.football.tab_content.all_competitions_categories.get_items(name=self.section_name_list)
            self.assertTrue(sections, msg=f'Competitions page does not have any "{self.section_name_list}" section')
            section = sections.get(self.section_name_list)
            self.assertTrue(section, msg=f'"{self.section_name_list}" section not found in "{sections.keys()}"')
            if not section.is_expanded():
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

            for tab_name, tab in self.tabs_menu.items_as_ordered_dict.items():
                self.assertIn(tab_name, vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values(),
                              msg='Market switcher tab is not present in the list')
            if vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches in [tab_name.upper() for tab_name in self.tabs_menu.items_as_ordered_dict.keys()]:
                current_tab = self.tabs_menu.current
                self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}"')

                self.assertTrue(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict,
                            msg=f'No events found on "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}" tab')

    def test_004_open_standings_tab(self):
        """
        DESCRIPTION: Open Standings tab
        EXPECTED: League Table with results is opened
        """
        if self.is_mobile:
            self.tabs_menu.click_button(vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings)
            current_tab = self.tabs_menu.current
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings}"')

    def test_005_check_page(self):
        """
        DESCRIPTION: Check page
        EXPECTED: - A ribbon with available sport types is displayed (Premier League, Championship etc) for the last season
        EXPECTED: - Arrows to switch season for league is displayed
        EXPECTED: - Table with results and statistics is shown
        """
        if self.is_mobile:
            competition_name = self.site.competition_league.title_section.type_name.text
            self.assertEqual(competition_name, self.league,
                             msg=f'Competition header with competition name is not same '
                                 f'Actual: "{competition_name}" '
                                 f'Expected: "{self.league}"')
            tab_content = self.site.competition_league.tab_content
            self.assertTrue(tab_content.previous_arrow.is_displayed(),
                            msg='Arrow to switch to previos season is not shown')

            self.assertTrue(tab_content.results_table.is_displayed(),
                            msg='Table with result was not found')

    def test_006_check_data_correctness_on_the_league_table_for_particular_seasoncompare_information_displayed_on_the_app_with_link_mentioned_in_pre_conditions(self):
        """
        DESCRIPTION: Check data correctness on the league table for particular season
        DESCRIPTION: Compare information displayed on the app with link mentioned in pre-conditions
        EXPECTED: The information is up to date
        """
        # Can not automate

    def test_007_for_desktopnavigate_to_football_landing_page___competitions_tab_and_select_any_competition_eg_premier_league(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Football Landing page -> 'Competitions' tab and select any Competition e.g. Premier League
        EXPECTED: * Competition Details page is opened
        EXPECTED: * League Table Widget is displayed in 3rd column or below main content area depending on screen resolution
        EXPECTED: * League Table Widget displays info about competition, user is viewing
        """
        if not self.is_mobile:
            wait_for_result(lambda : self.site.football.tabs_menu.click_button(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()), timeout=5)
            active_tab = self.site.football.tabs_menu.current
            self.assertEqual(active_tab, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper(),
                             msg=f'"{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()}" tab is not active, '
                                 f'active is "{active_tab}"')

            sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No countries found')
            if self.section_name_list.title() not in sections:
                grouping_buttons = self.site.football.tab_content.grouping_buttons.items_as_ordered_dict
                self.assertTrue(grouping_buttons, msg='No grouping buttons found')
                grouping_buttons[vec.sb_desktop.COMPETITIONS_SPORTS].click()

                sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(sections, msg='No countries found')
            if self.section_name_list not in ['USA', 'UEFA Club Competitions']:
                section_name = self.section_name_list if self.brand == 'bma' else self.section_name_list.title()
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

            self.assertTrue(self.site.competition_league.standings_widget.is_displayed(),
                            msg='Standings widget is not displayed')

    def test_008_for_desktopverify_header_and_sub_header_of_league_table_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Verify header and sub-header of League Table Widget
        EXPECTED: Header contains:
        EXPECTED: - 'League table' label and up/down facing chevron
        EXPECTED: - League Table Widget can be collapsed/expanded
        EXPECTED: Sub-header contains:
        EXPECTED: - season name of competition user is viewing (e.g. Premier League 17/18)
        EXPECTED: - left/right arrows to switch between seasons (no arrows in case of 1 season)
        """
        if not self.is_mobile:
            self.__class__.standings_widget = self.site.competition_league.standings_widget
            self.standings_widget.collapse()
            self.assertTrue(self.standings_widget.chevron_arrow.is_displayed(), msg='Chevron arrow is not displayed')
            self.standings_widget.expand()

            self.assertEqual(self.standings_widget.header_label, self.league_table_label,
                             msg=f'Label "{self.standings_widget.header_label}" '
                                 f'is not the same as expected "{self.league_table_label}"')

            self.assertTrue(self.standings_widget.season_name, msg='Season name is not displayed')
            self.assertTrue(self.standings_widget.previous_arrow.is_displayed(), msg='Previous arrow is not displayed')

    def test_009_for_desktopverify_table_data_and_footer(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Verify table data and footer
        EXPECTED: League Table contains info about first 5 teams with the following columns:
        EXPECTED: - POS (position in table)
        EXPECTED: - Team name (Text truncates for long names)
        EXPECTED: - P (stands for 'Plays/Matches total')
        EXPECTED: - W (stands for 'Won total')
        EXPECTED: - D (stands for 'Draw total')
        EXPECTED: - L (stands for 'Lost total')
        EXPECTED: - GD (stands for 'Goal Difference total')
        EXPECTED: - PTS (stands for 'Points total')
        EXPECTED: Footer contains 'Show all' link that on click expands to shown the rest of data. 'Show all' link changes to 'Show less'
        """
        if not self.is_mobile:
            self.assertEqual(self.standings_widget.table_headers, self.table_headers,
                             msg=f'"{self.standings_widget.table_headers}" table headers are not the same '
                                 f'as expected "{self.table_headers}"')
            self.assertEqual(self.standings_widget.row_number, self.default_row_number,
                             msg=f'Number of displayed rows "{self.standings_widget.row_number}" '
                                 f'is not the same as expected "{self.default_row_number}"')
            self.assertTrue(self.standings_widget.show_button.is_displayed(), msg='Show button is not displayed')
            self.standings_widget.show_button.click()
            result = wait_for_result(lambda: self.standings_widget.show_button.name == self.show_less_button_name,
                                     name='Show less button to be shown',
                                     timeout=2)
            self.assertTrue(result, msg='"Show less" button is not shown')

            self.assertLess(self.default_row_number, self.standings_widget.row_number,
                            msg=f'Number of displayed rows "{self.standings_widget.row_number}" '
                                f'is not bigger than "{self.default_row_number}"')

            self.assertTrue(result, msg=f'Show button name "{self.standings_widget.show_button.name}"'
                                        f' is not the same as expected "{self.show_less_button_name}"')

    def test_010_for_desktopswitch_to_a_different_competition_using_change_competition_selector_in_header(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Switch to a different competition using 'Change competition' selector in header
        EXPECTED: * Selected competition Details page is opened
        EXPECTED: * League Table Widget displays data of selected competition
        """
        if not self.is_mobile:
            current_section = self.site.competition_league.title_section.type_name.text
            self.site.competition_league.title_section.competition_selector_link.click()
            sections = self.site.competition_league.competitions_selector.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found in Competitions selector')

            for section_name, section in sections.items():
                section.click()
                leagues = section.league_selector.items_as_ordered_dict
                self.assertTrue(sections, msg='No leagues found in Leagues selector')
                for league_name, league in leagues.items():
                    if league_name.lower() != current_section.lower():
                        league.click()

                        self.site.wait_content_state('CompetitionLeaguePage')
                        league_name = league_name.upper() if self.brand == 'bma' else league_name
                        competition_title = self.site.competition_league.title_section.type_name.text
                        self.assertEqual(league_name, competition_title,
                                         msg=f'League name "{competition_title}"'
                                             f' is not the same as expected "{league_name}"')

                        self.assertTrue(self.site.competition_league.standings_widget.is_displayed(),
                                        msg='Standings widget is not displayed')
                        return
