import pytest
import tests
import voltron.environments.constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2 # removed ts2, stg2 markers due to result/standing tabs will be displayed for real events
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.reg165_fix
@vtest
class Test_C1200469_Verify_data_displayed_within_League_Table_Widget_for_Desktop(BaseSportTest):
    """
    TR_ID: C1200469
    NAME: Verify data displayed within League Table Widget for Desktop
    DESCRIPTION: This test case verifies data displayed within League Table Widget for Desktop
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
    PRECONDITIONS: Values in the League Table correspond to the following:
    PRECONDITIONS: P = "matchesTotal"
    PRECONDITIONS: W = "winTotal"
    PRECONDITIONS: D = "drawTotal"
    PRECONDITIONS: L = "lossTotal"
    PRECONDITIONS: GD = "goalDiffTotal"
    PRECONDITIONS: PTS = "pointsTotal"
    PRECONDITIONS: ![](index.php?/attachments/get/114765842)
    """
    keep_browser_open = True
    device_name = tests.desktop_default

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

    def test_004_verify_that_correct_competition_is_displayed_in_widget(self):
        """
        DESCRIPTION: Verify that correct competition is displayed in widget
        EXPECTED: Only data for competition, user is viewing, is displayed in widget
        EXPECTED: Use requests from preconditions for verification
        """
        self.__class__.standings_widget = self.site.competition_league.standings_widget
        self.assertTrue(self.standings_widget.season_name, msg='Season name is not displayed')
        season_name = self.standings_widget.season_name.split()
        competition = []
        for name in season_name:
            if not name.isdigit() and '/' not in name:
                competition.append(name)
        competition_name = ''.join(competition[0])
        self.assertIn(competition_name, ''.join(filter(str.isalnum, ''.join(self.league.split()))), msg="correct competition is not displayed in widget")

    def test_005_verify_a_list_of_seasons_for_viewed_competition(self):
        """
        DESCRIPTION: Verify a list of seasons for viewed competition
        EXPECTED: Request to verify a list of seasons with their IDs for selected competition:
        EXPECTED: **{domain}/seasons/1/XX/YY**,
        EXPECTED: where
        EXPECTED: * 1 - Spark category id for Football
        EXPECTED: * XX - Spark country id
        EXPECTED: * YY - Spark competitions id
        """
        seasons_list = []
        while not self.standings_widget.previous_arrow.is_displayed():
            seasons_list.append(self.standings_widget.season_name)
            self.standings_widget.previous_arrow.click()

    def test_006_verify_the_season_which_is_displayed_by_default(self):
        """
        DESCRIPTION: Verify the season which is displayed by default
        EXPECTED: All seasons are ordered by **startDate** attribute, following the rule: "The most recent season is opened by default"
        EXPECTED: Use **{domain}/api/seasons/1/XX/YY**  to see **startDate** attribute
        """
        # covered in step 5

    def test_007_verify_correct_results_are_shown_for_selected_season(self):
        """
        DESCRIPTION: Verify correct results are shown for selected season
        EXPECTED: Info is taken from the following request:
        EXPECTED: **{domain}/resultstables/1/XX/YY/ZZZZZ**,
        EXPECTED: where
        EXPECTED: * 1 - Spark category id for Football
        EXPECTED: * XX - Spark country id
        EXPECTED: * YY - Spark competitions id
        EXPECTED: * ZZZZZ - Spark season id
        """
        # covered in step 5

    def test_008_switch_between_seasons(self):
        """
        DESCRIPTION: Switch between seasons
        EXPECTED: * Call for another season is made
        EXPECTED: * Call for respective season results is made
        EXPECTED: * Corresponding information is displayed
        """
        # covered in step 5

    def test_009_switch_to_another_competition_using_change_competition_selector(self):
        """
        DESCRIPTION: Switch to another competition using 'Change Competition' selector
        EXPECTED: * Selected competition Details page is opened
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        EXPECTED: * League Table Widget is displayed in 3rd column
        """
        current_section = self.site.competition_league.title_section.type_name.text
        self.site.competition_league.title_section.competition_selector_link.click()
        sections = self.site.competition_league.competitions_selector.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found in Competitions selector')

        for section_name, section in sections.items():
            if section_name == vec.siteserve.ENGLAND:
                section.click()
                leagues = section.league_selector.items_as_ordered_dict
                self.assertTrue(sections, msg='No leagues found in Leagues selector')
                for league_name, league in leagues.items():
                    if league_name.lower() != current_section.lower():
                        league.click()

                        self.site.wait_content_state('CompetitionLeaguePage')
                        league_name = league_name.upper() if self.brand == 'bma' else league_name
                        self.assertEqual(league_name, self.site.competition_league.title_section.type_name.text,
                                         msg=f'League name "{self.site.competition_league.title_section.type_name.text}"'
                                             f' is not the same as expected "{league_name}"')

                        self.assertTrue(self.site.competition_league.standings_widget.is_displayed(),
                                        msg='Standings widget is not displayed')
                        return

    def test_010_repeat_steps_4_8(self):
        """
        DESCRIPTION: Repeat steps 4-8
        EXPECTED:
        """
        self.test_004_verify_that_correct_competition_is_displayed_in_widget()
        self.test_005_verify_a_list_of_seasons_for_viewed_competition()
