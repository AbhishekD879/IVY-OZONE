import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from time import sleep


# @pytest.mark.tst2 #can't execute on tst2 and stg2 due to result/standing tabs will be displayed for real events
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C2023952_Verify_Result_Widget_design_layout_for_Desktop(BaseSportTest):
    """
    TR_ID: C2023952
    NAME: Verify Result Widget design/layout for Desktop
    DESCRIPTION: This test case verifies Results Widget design/layout for Desktop.
    DESCRIPTION: Need to run test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: **Pre-conditions:**
    PRECONDITIONS: Results Widget is available ONLY for Football sport
    PRECONDITIONS: Use the following {domains} for different environments:
    PRECONDITIONS: * TST2: https://spark-br-tst.symphony-solutions.eu/api
    PRECONDITIONS: * STG2: https://spark-br-stg2.symphony-solutions.eu/api
    PRECONDITIONS: * PROD: https://spark-br.symphony-solutions.eu/api
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

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
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

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'Matches' tab is selected by default
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')

        current_tab_name = self.site.football.tabs_menu.current
        matches_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                   self.ob_config.football_config.category_id)
        self.assertEqual(current_tab_name, matches_tab_name,
                         msg=f'Default tab is "{current_tab_name}", it is not "{matches_tab_name}"')

    def test_003_choose_competitions_tab(self):
        """
        DESCRIPTION: Choose 'Competitions' tab
        EXPECTED: 'Competitions' tab is selected
        """
        competitions_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                        self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name, msg=f'"{competitions_tab_name}" tab is not active, '
                                                                f'active is "{active_tab}"')
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
        self.__class__.leagues = section.items_as_ordered_dict
        self.assertTrue(self.leagues, msg=f'No leagues found in the "{section_name_list}" section')

    def test_004_choose_some_competition_that_has_results_widget_from_expanded_class_accordion_and_click_it(self):
        """
        DESCRIPTION: Choose some competition that has 'Results' Widget from expanded 'Class' accordion and click it
        EXPECTED: * Competitions Details page is opened
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        EXPECTED: * 'Results' Widget is displayed in 3rd column or below main content (depends on screen resolution)
        """
        league = self.leagues.get(self.league)
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

        self.__class__.tabs_menu = self.site.competition_league.tabs_menu
        self.assertTrue(self.tabs_menu, msg='Tabs menu was not found')

        self.__class__.desktop_tabs = list(vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()) \
        if self.brand == 'bma' else [tab.title() for tab in vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()]
        for tab_name, tab in self.tabs_menu.items_as_ordered_dict.items():
            self.assertIn(tab_name, self.desktop_tabs,
                          msg=f'Market switcher tab {tab_name} is not present in the list')

        current_tab = self.tabs_menu.current
        self.assertEqual(current_tab, self.desktop_tabs[0],
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{self.desktop_tabs[0]}"')
        sleep(3)
        self.__class__.results_widget = self.site.competition_league.results_widget
        self.assertTrue(self.results_widget.is_displayed(), msg='Results widget is not displayed')

    def test_005_verify_header_accordion_of_result_widget(self):
        """
        DESCRIPTION: Verify header accordion of Result Widget
        EXPECTED: * Header contains capitalized text: 'Results' and up/down facing chevron
        EXPECTED: * Header accordion is collapsible/expandable to realize possibility of hiding/showing widget content
        EXPECTED: * On hover Header accordion color changes
        """
        self.assertTrue(self.results_widget.header_label, msg="'Results'text is not displayed")
        self.assertTrue(self.results_widget.collapse, msg="'Results' widget is not collapsible")
        self.assertTrue(self.results_widget.expand, msg="'Results' widget is not expandable")

    def test_006_verify_content_displaying_on_results_widget(self):
        """
        DESCRIPTION: Verify content displaying on 'Results' widget
        EXPECTED: 'Results' page/widget consists of:
        EXPECTED: * Results for different date is displayed in separate sections:
        EXPECTED: * Team 1/Team 2
        EXPECTED: * Score of Team 1/Score of Team 2
        EXPECTED: * Player_1 minute_1', minute_4'/Player_2 minute_1', minute_4'
        EXPECTED: * Date is displayed in the next format on each separate section: Today, Yesterday, 8th August 2018, etc.)
        """
        self.assertTrue(self.results_widget.team1, msg="Team1 is not displayed")
        self.assertTrue(self.results_widget.team2, msg="Team2 is not displayed")
        self.assertTrue(self.results_widget.team1_score, msg="Score of team1 is not displayed")
        self.assertTrue(self.results_widget.team2_score, msg="Score of team2 is not displayed")
        if self.brand == "Ladbrokes":
            self.assertTrue(self.results_widget.team1_scorer, msg="Scorer of team1 is not displayed")
            self.assertTrue(self.results_widget.team2_scorer, msg="Scorer of team2 is not displayed")

    def test_007_verify_footer_of_result_widget(self):
        """
        DESCRIPTION: Verify footer of Result Widget
        EXPECTED: Footer contains capitalized 'Show More' link
        """
        self.assertTrue(self.results_widget.show_button, msg="'Show More' link is not displayed")
