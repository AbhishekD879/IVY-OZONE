import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2 #can't execute on tst2 and stg2 due to result/standing tabs will be displayed for real events
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.reg156_fix
@vtest
class Test_C1406190_Verify_tabs_displaying_if_divisions_or_groups_are_available_for_League_on_League_Table_widget(BaseSportTest):
    """
    TR_ID: C1406190
    NAME: Verify tabs displaying if divisions or groups are available for League on 'League Table' widget
    DESCRIPTION: This test case verifies tabs displaying if divisions or groups are available for League on 'League Table' widget
    PRECONDITIONS: **Pre-conditions:**
    PRECONDITIONS: League Table Widget is available ONLY for Football sport
    PRECONDITIONS: Use the following {domains} for different environments:
    PRECONDITIONS: * TST: https://stats-centre-tst0.coral.co.uk/api
    PRECONDITIONS: * PROD: https://stats-centre.coral.co.uk/api/
    PRECONDITIONS: **Requests:**
    PRECONDITIONS: Request to get Spark id for competition user is viewing (see value in “competitionId”):
    PRECONDITIONS: **{domain}/brcompetitionseason/XX/YY/ZZZ**,
    PRECONDITIONS: where
    PRECONDITIONS: * XX - OB category id (e.g. Football - id=16)
    PRECONDITIONS: * YY - OB class id (e.g. Football England - id=97)
    PRECONDITIONS: * ZZZ - OB type id (e.g. Premier League - id=442)
    PRECONDITIONS: A list of seasons with their IDs for selected competition:
    PRECONDITIONS: **{domain}/seasons/1/XX/YY**,
    PRECONDITIONS: where
    PRECONDITIONS: * 1 - Spark category id for Football
    PRECONDITIONS: * XX - Spark country id
    PRECONDITIONS: * YY - Spark competitions id
    PRECONDITIONS: Results for selected season:
    PRECONDITIONS: **{domain}/resultstables/1/XX/YY/ZZZZZ**,
    PRECONDITIONS: where
    PRECONDITIONS: * 1 - Spark category id for Football
    PRECONDITIONS: * XX - Spark country id
    PRECONDITIONS: * YY - Spark competitions id
    PRECONDITIONS: * ZZZZZ - Spark season id
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    table_headers = ['POS', '', 'P', 'W', 'D', 'L', 'GD', 'PTS']
    default_row_number = 5

    def test_000_preconditions(self):
        event = self.get_competition_with_results_and_standings_tabs(
            category_id=self.ob_config.football_config.category_id, raise_exceptions=True)
        sport_name = event.class_name.upper().split(" ")
        if sport_name[0] == vec.sb.FOOTBALL.upper():
            self.__class__.section_name_list = sport_name[1]
        else:
            self.__class__.section_name_list = sport_name[0]
        self.__class__.league = event.league_name

        self.__class__.league_table_label = vec.sb.LEAGUE_TABLE_LABEL.title() if self.brand == 'bma' else vec.sb.LEAGUE_TABLE_LABEL

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.site.wait_content_state("HomePage")

    def test_002_navigate_to_football_landing_page___competitions_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -> 'Competitions' tab
        EXPECTED: Competitions Landing page is opened
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name=vec.sb.FOOTBALL)

    def test_003_expand_classes_accordion_and_select_group_stage_league_ie_the_international_class_euro_cup_league_or_league_with_separate_division_ie_usa_class_major_league_soccer_type(self):
        """
        DESCRIPTION: Expand Classes accordion and select Group Stage League (ie. the 'International' class, 'Euro Cup' league) or League with Separate Division (ie. 'USA' class, 'Major League Soccer' type)
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        EXPECTED: * League Table Widget is displayed in 3rd column
        """
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper(),
                         msg=f'"{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper()}" tab is not active, '
                         f'active is "{active_tab}"')

        self.site.football.tabs_menu.click_button(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper())
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

        self.__class__.standings_widget = self.site.competition_league.standings_widget
        self.standings_widget.collapse()
        self.assertTrue(self.standings_widget.chevron_arrow.is_displayed(), msg='Chevron arrow is not displayed')
        self.standings_widget.expand()

        self.assertEqual(self.standings_widget.header_label, self.league_table_label,
                         msg=f'Label "{self.standings_widget.header_label}" '
                         f'is not the same as expected "{self.league_table_label}"')

        self.assertTrue(self.standings_widget.season_name, msg='Season name is not displayed')
        self.assertTrue(self.standings_widget.previous_arrow.is_displayed(), msg='Previous arrow is not displayed')

    def test_004_verify_displaying_of_groupdivision_tabs(self):
        """
        DESCRIPTION: Verify displaying of 'Group'/'Division' tabs
        EXPECTED: * 'Group'/'Division' tabs are displayed below Sub Header with the league name
        EXPECTED: * The first one is selected by default and highlighted
        EXPECTED: * The name of tabs corresponds to value in 'tableName' attribute received in response to the particular season
        EXPECTED: * Data received from the response to the particular season is displayed below the selected 'Group'/'Division' tab
        """
        sub_tabs = self.standings_widget.sub_tabs.items
        self.assertTrue(sub_tabs, msg='"Sub tabs" is not displayed')
        actual_current_tab = self.standings_widget.sub_tabs.selected_item
        expected_current_tab = self.standings_widget.sub_tabs.items[0].name
        self.assertEqual(actual_current_tab, expected_current_tab,
                         msg=f'Actual current tab"{actual_current_tab}" is not equal to'
                             f'Expected current tab"{expected_current_tab}"')

    def test_005_hover_the_mouse_over_the_groupdivision_tabs(self):
        """
        DESCRIPTION: Hover the mouse over the 'Group'/'Division' tabs
        EXPECTED: * Navigation arrows do NOT appear in case all tabs are visible fully
        EXPECTED: * Navigation arrows appear in case NOT all tabs are visible fully
        """
        # cant automate this step due no events with all tabs are not visible fully

    def test_006_click_on_navigation_arrows_to_rich_the_groupdivision_tab_that_is_not_visible_fully_or_not_visible_at_all(self):
        """
        DESCRIPTION: Click on Navigation arrows to rich the 'Group'/'Division' tab that is not visible fully or not visible at all
        EXPECTED: Content scrolls horizontally in the left or right directions
        """
        # cant automate this step due no events with all tabs are not visible fully

    def test_007_click_on_some_groupdivision_tab(self):
        """
        DESCRIPTION: Click on some 'Group'/'Division' tab
        EXPECTED: * 'Group'/'Division' tab is clickable
        EXPECTED: * Selected 'Group'/'Division' tab is highlighted
        EXPECTED: * Data received from the response to the particular season is displayed below the selected 'Group'/'Division' tab
        """
        for i in range(0, len(self.standings_widget.sub_tabs.items)):
            self.standings_widget.sub_tabs.items[i].click()
            no_events = self.standings_widget.has_no_events_label()
            if not no_events:
                self.assertTrue(self.standings_widget.sub_tabs.items[i].name, msg=f'"Tab Name is not displayed"')
                self.assertEqual(self.standings_widget.table_headers, self.table_headers,
                                 msg=f'"{self.standings_widget.table_headers}" table headers are not the same '
                                     f'as expected "{self.table_headers}"')
                if self.site.competition_league.standings_widget.has_show_button():
                    self.assertLessEqual(self.standings_widget.row_number, self.default_row_number,
                                 msg=f'Number of displayed rows "{self.standings_widget.row_number}" '
                                     f'is not the same as expected "{self.default_row_number}"')
            else:
                self.assertTrue(no_events, msg='Results are currently available for this league')

    def test_008_click_on_groupdivision_tab_that_not_contains_any_data(self):
        """
        DESCRIPTION: Click on 'Group'/'Division' tab that not contains any data
        EXPECTED: * 'Group'/'Division' tab is clickable
        EXPECTED: * Selected 'Group'/'Division' tab is highlighted
        EXPECTED: * 'Data not found' received in the response to the particular 'Group'/'Division'
        EXPECTED: * 'No events found' message is displayed below the selected 'Group'/'Division' tab
        """
        # covered into step 7
