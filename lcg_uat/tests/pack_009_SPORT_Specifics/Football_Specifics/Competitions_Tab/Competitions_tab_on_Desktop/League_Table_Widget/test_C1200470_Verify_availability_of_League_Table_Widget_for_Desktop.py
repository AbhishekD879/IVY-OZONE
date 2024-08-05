import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


# @pytest.mark.tst2 #can't execute on tst2 and stg2 due to result/standing tabs will be displayed for real events
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C1200470_Verify_availability_of_League_Table_Widget_for_Desktop(BaseSportTest):
    """
    TR_ID: C1200470
    NAME: Verify availability of 'League Table' Widget for Desktop
    DESCRIPTION: This test case verifies conditions when 'League Table' Widget is shown/hidden for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: **Pre-conditions:**
    PRECONDITIONS: League Table Widget is available ONLY for Football sport
    PRECONDITIONS: Use the following {domains} for different environments:
    PRECONDITIONS: * TST: https://stats-centre-tst0.coral.co.uk/api
    PRECONDITIONS: * PROD: https://stats-centre.coral.co.uk/api/
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
    PRECONDITIONS: * ZZZZZ - Spark season id**Pre-conditions:**
    PRECONDITIONS: League Table Widget is available ONLY for Football sport
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def verify_results_widget_position(self, width, height):
        self.device.set_viewport_size(width=width, height=height)
        results_widget = self.site.competition_league.results_widget
        self.assertTrue(results_widget.is_displayed(), msg='Results widget is not displayed')

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
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper(),
                         msg=f'"{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper()}" tab is not active, '
                             f'active is "{active_tab}"')

    def test_003_navigate_to_any_competition_details_page_that_has_league_table_widget(self):
        """
        DESCRIPTION: Navigate to any Competition Details page that has 'League Table' Widget
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        EXPECTED: * 'League Table' Widget is displayed in 3rd column
        """
        self.site.football.tabs_menu.click_button(self.expected_sport_tabs.competitions)
        current_tab_name = self.site.football.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.competitions,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected tab: "{self.expected_sport_tabs.matches}"')
        football = self.site.football.tab_content
        grouping_buttons = football.grouping_buttons
        grouping_buttons.click_item(vec.sb_desktop.COMPETITIONS_SPORTS)
        sections = football.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Sections not found')
        self.assertTrue(grouping_buttons.items_as_ordered_dict, msg='No grouping buttons found')

        section_name_list = self.section_name_list.title() if self.brand == 'ladbrokes' else self.section_name_list
        section = sections.get(section_name_list)
        self.assertTrue(section, msg=f'"{section_name_list}" was not found')
        section.expand()
        self.assertTrue(section.is_expanded(), msg=f'Section "{section_name_list}" is not expanded')
        leagues = section.items_as_ordered_dict
        self.assertTrue(leagues, msg=f'No leagues found in the "{section_name_list}" section')

        leagues.get(self.league).click()
        self.site.wait_content_state('CompetitionLeaguePage', timeout=20)
        sleep(3)
        self.assertTrue(self.site.competition_league.standings_widget.is_displayed(),
                        msg='Standings widget is not displayed')

        standings_widget = self.site.competition_league.standings_widget
        standings_widget.collapse()
        self.assertTrue(standings_widget.chevron_arrow.is_displayed(), msg='Chevron arrow is not displayed')
        standings_widget.expand()

        self.assertEqual(standings_widget.header_label, self.league_table_label,
                         msg=f'Label "{standings_widget.header_label}" '
                             f'is not the same as expected "{self.league_table_label}"')

        self.assertTrue(standings_widget.season_name, msg='Season name is not displayed')
        self.assertTrue(standings_widget.previous_arrow.is_displayed(), msg='Previous arrow is not displayed')

    def test_004_switch_to_outrights_tab(self):
        """
        DESCRIPTION: Switch to 'Outrights' tab
        EXPECTED: * List of Outrights events is loaded on the page
        EXPECTED: * 'League Table' Widget is displayed in 3rd column
        """
        tabs = list(self.site.competition_league.tabs_menu.items_as_ordered_dict.keys())
        outrights = 'OUTRIGHTS' if self.brand == 'bma' else 'Outrights'
        if outrights in tabs:
            self.site.competition_league.tabs_menu.items_as_ordered_dict.get(outrights).click()
            outright_events = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(outright_events, msg='No outrights events found')
            results_widget = self.site.competition_league.results_widget
            self.assertTrue(results_widget.is_displayed(), msg='Results widget is not displayed')
            self.verify_results_widget_position(width=1280, height=1300)
            self.verify_results_widget_position(width=1279, height=1200)

    def test_005_verify_position_of_league_table_widget(self):
        """
        DESCRIPTION: Verify position of 'League Table' Widget
        EXPECTED: * 'League Table' Widget is shown in 3rd column at 1280px and higher screen resolution
        EXPECTED: * 'League Table' Widget is shown in 2nd column below the list of competition events at 1279px and lower screen resolutions
        """
        # Covered in above step

    def test_006_verify_condition_when_league_table_widget_is_shown(self):
        """
        DESCRIPTION: Verify condition when 'League Table' Widget is shown
        EXPECTED: 'League Table' Widget is shown in case data for selected competition/season is received from Spark.
        EXPECTED: Use this request to verify:
        EXPECTED: **{domain}/resultstables/1/XX/YY/ZZZZZ**,
        EXPECTED: where
        EXPECTED: * 1 - Spark category id for Football
        EXPECTED: * XX - Spark country id
        EXPECTED: * YY - Spark competitions id
        EXPECTED: * ZZZZZ - Spark season id
        EXPECTED: In case 'Data not found' is returned ('Preview' tab), widget is NOT shown
        """
        # Out of scope

    def test_007_navigate_to_competition_details_page_for_which_data_is_not_received(self):
        """
        DESCRIPTION: Navigate to Competition Details page for which data is not received
        EXPECTED: * 'League Table' Widget is not shown
        EXPECTED: * 'Results' Widget is shown in case it's available
        EXPECTED: * 2nd column extends to occupy 3rd column in case none of the widgets available
        """
        # Out of scope
