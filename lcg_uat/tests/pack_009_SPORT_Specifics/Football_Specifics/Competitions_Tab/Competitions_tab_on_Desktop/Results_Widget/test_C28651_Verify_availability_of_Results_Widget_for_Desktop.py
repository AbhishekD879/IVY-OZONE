import pytest
import tests
from time import sleep
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


# @pytest.mark.tst2  #can't execute on tst2 and stg2 due to result/standing tabs will be displayed for real events
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C28651_Verify_availability_of_Results_Widget_for_Desktop(BaseSportTest):
    """
    TR_ID: C28651
    NAME: Verify availability of 'Results' Widget for Desktop
    DESCRIPTION: This test case verifies availability of 'Results' Widget for Desktop.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: **Pre-conditions:**
    PRECONDITIONS: Results Widget is available ONLY for Football sport
    PRECONDITIONS: Use the following {domains} for different environments:
    PRECONDITIONS: * TST2: https://spark-br-tst.symphony-solutions.eu/api
    PRECONDITIONS: * STG2: https://spark-br-stg2.symphony-solutions.eu/api
    PRECONDITIONS: * PROD: https://spark-br.symphony-solutions.eu/api
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
    PRECONDITIONS: Results for the selected season:
    PRECONDITIONS: **{domain}/season/XXXXX/matches/?skip=0&limit=4** for desktop OR **limit=8** for mobile,
    PRECONDITIONS: where
    PRECONDITIONS: * XXXXX - Spark season id
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def verify_results_widget_position(self, width, height):
        self.device.set_viewport_size(width=width, height=height)
        results_widget = self.site.competition_league.results_widget
        self.assertTrue(results_widget.is_displayed(), msg='Results widget is not displayed')

    def test_000_preconditions(self):
        event = self.get_competition_with_results_and_standings_tabs(
            category_id=self.ob_config.football_config.category_id, raise_exceptions=True)
        sport_name = event.class_name.upper().split(" ")
        if sport_name[0] == vec.siteserve.FOOTBALL_TAB.upper():
            self.__class__.section_name_list = sport_name[1]
        else:
            self.__class__.section_name_list = sport_name[0]
        self.__class__.league = event.league_name
        self.__class__.type_id = event.type_id
        self.__class__.is_mobile = self.device_type == 'mobile'

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'Matches' tab is selected by default
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        current_tab_name = self.site.football.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.matches,
                         msg=f'Default tab is not "{self.expected_sport_tabs.matches}", it is "{current_tab_name}"')

    def test_003_choose_competitions_tab(self):
        """
        DESCRIPTION: Choose 'Competitions' tab
        EXPECTED: 'Competitions' tab is selected
        """
        self.site.football.tabs_menu.click_button(self.expected_sport_tabs.competitions)
        current_tab_name = self.site.football.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.competitions,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected tab: "{self.expected_sport_tabs.matches}"')

    def test_004_choose_some_competition_that_has_results_widget_from_expanded_class_accordion_and_clicktap_it(self):
        """
        DESCRIPTION: Choose some competition that has 'Results' Widget from expanded 'Class' accordion and click/tap it
        EXPECTED: * Competitions Details page is opened
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        EXPECTED: * 'Results' Widget is displayed in 3rd column
        """
        football = self.site.football.tab_content
        grouping_buttons = football.grouping_buttons
        grouping_buttons.click_item(vec.sb_desktop.COMPETITIONS_SPORTS)
        self.__class__.sections = football.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='Sections not found')
        self.assertTrue(grouping_buttons.items_as_ordered_dict, msg='No grouping buttons found')

        section_name_list = self.section_name_list.title() if not self.is_mobile and self.brand == 'ladbrokes' else self.section_name_list
        section = self.sections.get(section_name_list)
        self.assertTrue(section, msg=f'"{section_name_list}" was not found')
        section.expand()
        self.assertTrue(section.is_expanded(), msg=f'Section "{section_name_list}" is not expanded')
        leagues = section.items_as_ordered_dict
        self.assertTrue(leagues, msg=f'No leagues found in the "{section_name_list}" section')

        leagues.get(self.league).click()
        self.site.wait_content_state('CompetitionLeaguePage')

        tabs_menu = self.site.competition_league.tabs_menu
        self.assertTrue(tabs_menu, msg='Tabs menu was not found')

        self.__class__.desktop_tabs = list(vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()) \
            if self.brand == 'bma' else [tab.title() for tab in vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()]
        for tab_name, tab in tabs_menu.items_as_ordered_dict.items():
            self.assertIn(tab_name, self.desktop_tabs,
                          msg=f'Market switcher tab {tab_name} is not present in the list')

        current_tab = tabs_menu.current
        self.assertEqual(current_tab, self.desktop_tabs[0],
                         msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                             f'expected "{self.desktop_tabs[0]}"')
        sleep(3)
        results_widget = self.site.competition_league.results_widget
        self.assertTrue(results_widget.is_displayed(), msg='Results widget is not displayed')

    def test_005_switch_to_outrights_tab(self):
        """
        DESCRIPTION: Switch to 'Outrights' tab
        EXPECTED: * List of Outrights events is loaded on the page
        EXPECTED: * 'Results' Widget is displayed in 3rd column
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

    def test_006_verify_position_of_results_widget(self):
        """
        DESCRIPTION: Verify position of 'Results' Widget
        EXPECTED: * 'Results' Widget is shown in 3rd column at 1280px and higher screen resolution
        EXPECTED: * 'Results' Widget is shown in 2nd column below the list of competition events at 1279px and lower screen resolutions
        """
        # Covered in above step

    def test_007_verify_condition_when_results_widget_is_shown(self):
        """
        DESCRIPTION: Verify condition when 'Results' Widget is shown
        EXPECTED: 'Results' Widget is shown in case data for selected competition/season is received from Spark.
        EXPECTED: Use this request to verify:
        EXPECTED: **{domain}/season/XXXXX/matches/?skip=0&limit=4**
        EXPECTED: where
        EXPECTED: * XXXXX - Spark season id
        EXPECTED: In case 'Data not found' is returned ('Preview' tab), widget is NOT shown
        """
        # Out of scope

    def test_008_navigate_to_competition_details_page_for_which_data_is_not_received(self):
        """
        DESCRIPTION: Navigate to Competition Details page for which data is not received
        EXPECTED: * 'Results' Widget is not shown
        EXPECTED: * 'League Table' Widget is shown in case it's available
        EXPECTED: * 2nd column extends to occupy 3rd column in case none of the widgets available
        """
        # Out of scope
