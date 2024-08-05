import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from voltron.utils.waiters import wait_for_result
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


# @pytest.mark.tst2  # result/standing tabs will be displayed for real events
# @pytest.mark.stg2  # result/standing tabs will be displayed for real events
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.mobile_only
@pytest.mark.sanity
@vtest
class Test_C10278996_Competition_Standings(BaseSportTest):
    """
    TR_ID: C10278996
    NAME: Competition Standings.
    DESCRIPTION: Test case verifies Standings tab on Competitions (which substituted 'Leagues' page in OX 98)
    PRECONDITIONS: **User is on Football > Competitions tab**
    PRECONDITIONS: Link to check league table results: http://www.espnfc.com/english-league-championship/24/table
    """
    keep_browser_open = True
    table_headers = ['Team', 'P', 'W', 'D', 'L', 'GD', 'Pts']

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
        self.__class__.league_table_label = vec.sb.LEAGUE_TABLE_LABEL.title() if self.brand == 'bma' else vec.sb.LEAGUE_TABLE_LABEL

        self.site.open_sport(name=self.get_sport_title(category_id=self.ob_config.football_config.category_id).upper())
        self.site.wait_content_state(state_name=vec.sb.FOOTBALL)
        self.site.football.tabs_menu.click_button(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper())
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper(),
                         msg=f'"{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()}" tab is not active, '
                             f'active is "{active_tab}"')

    def test_001_select_competitionverify_standings_tab(self):
        """
        DESCRIPTION: Select competition
        DESCRIPTION: Verify Standings tab
        EXPECTED: Standings tab is present on Competition page if data is returned from 'resultstables' query
        """
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
        sleep(5)
        self.site.wait_content_state('CompetitionLeaguePage')
        self.__class__.tabs_menu = self.site.competition_league.tabs_menu
        self.assertTrue(self.tabs_menu, msg='Tabs menu was not found')
        self.assertIn(vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings, self.tabs_menu.items_as_ordered_dict.keys(),
                      msg=f'"{vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings}" is not present in Competitions Page')

        self.tabs_menu.click_button(vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings)
        current_tab = self.tabs_menu.current
        self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings,
                         msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                             f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings}"')

    def test_002_verify_table(self):
        """
        DESCRIPTION: Verify Table
        EXPECTED: - League Table is given for the current season of selected Competition
        EXPECTED: - Table contains the following columns:
        EXPECTED: POS (position in table)
        EXPECTED: Team name (Text truncates for long names)
        EXPECTED: P (stands for 'Plays/Matches total')
        EXPECTED: W (stands for 'Won total')
        EXPECTED: D (stands for 'Draw total')
        EXPECTED: L (stands for 'Lost total')
        EXPECTED: GD (stands for 'Goal Difference total')
        EXPECTED: PTS (stands for 'Points total')
        """
        tab_content = self.site.competition_league.tab_content
        self.assertEqual(tab_content.table_headers, self.table_headers,
                         msg=f'"{tab_content.table_headers}" table headers are not the same '
                             f'as expected "{self.table_headers}"')

    def test_003_verify_user_can_navigate_between_available_seasons(self):
        """
        DESCRIPTION: Verify user can navigate between available seasons
        EXPECTED: User can navigate using arrow in the Table header
        EXPECTED: for ex. from UEFA Champions League 18/19 to UEFA Champions League 17/18 and back
        """
        tab_content = self.site.competition_league.tab_content
        self.assertTrue(tab_content.previous_arrow.is_displayed(),
                        msg='Arrow to switch to previous season is not shown')
        season_name_bfr_clk = tab_content.season_name
        tab_content.previous_arrow.click()
        wait_for_result(lambda: season_name_bfr_clk != self.site.competition_league.tab_content.season_name,
                        name='Waiting for Season to change',
                        timeout=15)
        season_name_aftr_clk = tab_content.season_name
        self.assertNotEqual(season_name_bfr_clk, season_name_aftr_clk,
                            msg=f'Season Before click "{season_name_bfr_clk}"  Season after click "{season_name_aftr_clk}"')
