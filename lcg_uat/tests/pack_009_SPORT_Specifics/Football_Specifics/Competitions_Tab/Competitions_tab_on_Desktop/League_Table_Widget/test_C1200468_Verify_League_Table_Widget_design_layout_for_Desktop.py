import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.desktop
# @pytest.mark.tst2 #can't execute on tst2 and stg2 redue to result/standing tabs will be displayed for real events
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C1200468_Verify_League_Table_Widget_design_layout_for_Desktop(BaseSportTest):
    """
    TR_ID: C1200468
    NAME: Verify League Table Widget design/layout for Desktop
    DESCRIPTION: This test case verifies League Table Widget design/layout for Desktop.
    DESCRIPTION: Need to run test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    DESCRIPTION: https://app.zeplin.io/project/59f0b3bf277e469f985e211d/screen/5a37a27592b402caa8eb4f4b
    PRECONDITIONS: **Pre-conditions:**
    PRECONDITIONS: League Table Widget is available ONLY for Football sport
    PRECONDITIONS: Use the following {​​​​​​​​domains}​​​​​​​​ for different environments:
    PRECONDITIONS: * TST: https://stats-centre-tst0.coral.co.uk/api
    PRECONDITIONS: * PROD: https://stats-centre.coral.co.uk/api/
     """
    keep_browser_open = True
    device_name = tests.desktop_default
    table_headers = ['POS', '', 'P', 'W', 'D', 'L', 'GD', 'PTS']
    default_row_number = 5
    show_less_button_name = vec.big_competitions.SHOW_LESS.upper()
    show_more_button_name = vec.SB.SHOW_ALL.upper()

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        event = self.get_competition_with_results_and_standings_tabs(
            category_id=self.ob_config.football_config.category_id, raise_exceptions=True)
        sport_name = event.class_name.upper().split(" ")
        if sport_name[0] == vec.sb.FOOTBALL.upper():
            self.__class__.section_name_list = sport_name[1]
        else:
            self.__class__.section_name_list = sport_name[0]
        self.__class__.league = event.league_name

        self.__class__.league_table_label = vec.sb.LEAGUE_TABLE_LABEL.title() if self.brand == 'bma' else vec.sb.LEAGUE_TABLE_LABEL
        self.site.wait_content_state("HomePage")

    def test_002_navigate_to_football_landing_page___competitions_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -> 'Competitions' tab
        EXPECTED: Competitions Landing page is opened
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name=vec.sb.FOOTBALL)

    def test_003_expand_any_classes_accordion_and_select_any_type_competition(self):
        """
        DESCRIPTION: Expand any Classes accordion and select any Type (Competition)
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        EXPECTED: * League Table Widget is displayed in 3rd column
        """
        # covered in step 4

    def test_004_verify_header_accordion_of_league_table_widget(self):
        """
        DESCRIPTION: Verify header accordion of League Table Widget
        EXPECTED: * Header contains capitalized text: 'League Table' and up/down facing chevron
        EXPECTED: * Header accordion is collapsible/expandable to realize possibility of hiding/showing widget content
        EXPECTED: * On hover Header accordion color changes
        """
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

    def test_005_verify_sub_header_of_league_table_widget(self):
        """
        DESCRIPTION: Verify sub header of League Table Widget
        EXPECTED: Sub header contains:
        EXPECTED: * season name of competition user is viewing (e.g. Championship 17/18)
        EXPECTED: * left/right arrows in case of multiple seasons within the same competition
        EXPECTED: * no arrows are displayed in case of 1 season
        """
        self.__class__.standings_widget = self.site.competition_league.standings_widget
        self.standings_widget.collapse()
        self.assertTrue(self.standings_widget.chevron_arrow.is_displayed(), msg='Chevron arrow is not displayed')
        self.standings_widget.expand()

        self.assertEqual(self.standings_widget.header_label, self.league_table_label,
                         msg=f'Label "{self.standings_widget.header_label}" '
                         f'is not the same as expected "{self.league_table_label}"')

        self.assertTrue(self.standings_widget.season_name, msg='Season name is not displayed')
        self.assertTrue(self.standings_widget.previous_arrow.is_displayed(), msg='Previous arrow is not displayed')

    def test_006_verify_table_data(self):
        """
        DESCRIPTION: Verify table data
        EXPECTED: League Table contains info about first 5 teams with the following columns:
        EXPECTED: * POS (position in table)
        EXPECTED: * Team name (Text truncates for long names)
        EXPECTED: * P (stands for 'Plays/Matches total')
        EXPECTED: * W (stands for 'Won total')
        EXPECTED: * D (stands for 'Draw total')
        EXPECTED: * L (stands for 'Lost total')
        EXPECTED: * GD (stands for 'Goal Difference total')
        EXPECTED: * PTS (stands for 'Points total')
        """
        self.assertEqual(self.standings_widget.table_headers, self.table_headers,
                         msg=f'"{self.standings_widget.table_headers}" table headers are not the same '
                         f'as expected "{self.table_headers}"')
        self.assertEqual(self.standings_widget.row_number, self.default_row_number,
                         msg=f'Number of displayed rows "{self.standings_widget.row_number}" '
                         f'is not the same as expected "{self.default_row_number}"')

    def test_007_verify_footer_of_league_table_widget(self):
        """
        DESCRIPTION: Verify footer of League Table Widget
        EXPECTED: * Footer contains capitalized 'Show all' link
        """
        self.assertTrue(self.standings_widget.show_button.is_displayed(), msg='Show button is not displayed')

    def test_008_click_on_show_all_link(self):
        """
        DESCRIPTION: Click on 'Show all' link
        EXPECTED: * Widget expands downwards to show full League Table
        EXPECTED: * 'Show all' changes to 'Show less'
        """
        self.standings_widget.show_button.click()
        result = wait_for_result(lambda: self.standings_widget.show_button.name == self.show_less_button_name,
                                 name='Show less button to be shown',
                                 timeout=2)
        self.assertTrue(result, msg='"Show less" button is not shown')

    def test_009_click_on_show_less_link(self):
        """
        DESCRIPTION: Click on 'Show less' link
        EXPECTED: * Widget collapses to show first 5 teams
        EXPECTED: * 'Show less' changes to 'Show all'
        """
        self.standings_widget.show_button.click()
        result = wait_for_result(lambda: self.standings_widget.show_button.name == self.show_more_button_name,
                                 name='Show less button to be shown',
                                 timeout=2)
        self.assertTrue(result, msg='"Show all" button is not shown')
