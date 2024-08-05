import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2 # removed ts2, stg2 markers due to result/standing tabs will be displayed for real events
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C9608052_Verify_Standings_tab_behaivior_on_Competition_details_page(BaseSportTest):
    """
    TR_ID: C9608052
    NAME: Verify 'Standings' tab behaivior on Competition details page
    DESCRIPTION: This test case verifies 'Standings' tab displayed on Football competition details page depends on league table availability
    PRECONDITIONS: 1. Navigate to Football landing page > Competitions tab
    PRECONDITIONS: 2. Expand any class accordion and click on any type (e.g. Premier League)
    PRECONDITIONS: NOTE:
    PRECONDITIONS: 'Standings' tab is displayed if a league table is available for that league on the competition page(received from Bet Radar)
    PRECONDITIONS: **Requests:**
    PRECONDITIONS: Request to get Spark id for competition user is viewing (see value in “competitionId”):
    PRECONDITIONS: **/brcompetitionseason/XX/YY/ZZZ,**
    PRECONDITIONS: where
    PRECONDITIONS: * XX - OB category id (e.g. Football - id=16)
    PRECONDITIONS: * YY - OB class id (e.g. Football England - id=97)
    PRECONDITIONS: * ZZZ - OB type id (e.g. Premier League - id=442)
    PRECONDITIONS: Request to get league table for competition user is viewing (see value in “competitionId”):
    PRECONDITIONS: **/resultstables/X/YY/HH/ZZZZ,**
    PRECONDITIONS: where
    PRECONDITIONS: * X - OB area Id (e.g England id=1)
    PRECONDITIONS: * YY - OB competition Id (e.g Premier League id=1)
    PRECONDITIONS: * HH - OB sport Id (e.g Soccer id=1)
    PRECONDITIONS: * ZZZZ - OB season Id(e.g. id = 38738)
    """
    keep_browser_open = True

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
        self.navigate_to_page("sport/football")
        self.site.wait_content_state(state_name=vec.sb.FOOTBALL)
        if self.is_mobile:
            self.site.football.tabs_menu.click_button(
                self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper())
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

            current_tab = self.tabs_menu.current
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}"')

            self.assertTrue(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict,
                            msg=f'No events found on "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}" tab')
        else:
            self.site.football.tabs_menu.click_button(
                self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper())
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

    def test_001_tap_standings_tab(self):
        """
        DESCRIPTION: Tap 'Standings' tab
        EXPECTED: * User navigates to the appropriate competition page (e.g. Premier League)
        EXPECTED: * The league table for that competition for current season is displayed
        """
        if self.is_mobile:
            self.tabs_menu.click_button(vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings)
            current_tab = self.tabs_menu.current
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings}"')

    def test_002_navigate_to_previous_league_tableif_one_is_available(self):
        """
        DESCRIPTION: Navigate to previous League Table(if one is available)
        EXPECTED: User is navigated to page with the previous league table for that competition when multiple league tables are received
        """
        if self.is_mobile:
            tab_content = self.site.competition_league.tab_content
            current_league = tab_content.season_name
            if tab_content.previous_arrow.is_displayed():
                self.assertTrue(tab_content.previous_arrow.is_displayed(),
                                msg='Arrow to switch to previos season is not shown')
                self.site.competition_league.tab_content.previous_arrow.click()
                self.assertTrue(self.site.competition_league.tab_content.results_table.is_displayed(),
                                msg='Table with result was not found')
                previous_league = self.site.competition_league.tab_content.season_name
                self.site.contents.scroll_to_top()
                self.assertNotEqual(previous_league, current_league, msg='User is not navigating to previous league')
                self.site.competition_league.tab_content.next_arrow.click()
                league_name = self.site.competition_league.tab_content.season_name
                self.site.contents.scroll_to_top()
                self.assertEqual(current_league, league_name, msg='user is not navigating to curret league')
            else:
                self._logger.info(msg='there is no previous league table available')
        else:
            standings_widget = self.site.competition_league.standings_widget
            standings_widget.collapse()
            self.assertTrue(standings_widget.chevron_arrow.is_displayed(), msg='Chevron arrow is not displayed')
            standings_widget.expand()
            self.assertEqual(standings_widget.header_label, self.league_table_label,
                             msg=f'Label "{standings_widget.header_label}" '
                                 f'is not the same as expected "{self.league_table_label}"')
            current_league = self.site.competition_league.standings_widget.season_name
            if standings_widget.previous_arrow.is_displayed():
                self.site.competition_league.standings_widget.previous_arrow.click()
                sleep(3)
                previous_league = self.site.competition_league.standings_widget.season_name
                self.assertNotEqual(previous_league, current_league, msg='User is not navigating to previous league')
                self.site.competition_league.standings_widget.next_arrow.click()
                sleep(2)
                league_name = self.site.competition_league.standings_widget.season_name
                sleep(3)
                self.assertEqual(current_league, league_name, msg='user is not navigating to current league')
            else:
                self._logger.info(msg='there is no previous league table available')

    def test_003_navigate_to_current_league_table_if_viewing_a_previous_one(self):
        """
        DESCRIPTION: Navigate to current League Table (if viewing a previous one)
        EXPECTED: User is navigated to the current League Table
        """
        # covered in step 002
