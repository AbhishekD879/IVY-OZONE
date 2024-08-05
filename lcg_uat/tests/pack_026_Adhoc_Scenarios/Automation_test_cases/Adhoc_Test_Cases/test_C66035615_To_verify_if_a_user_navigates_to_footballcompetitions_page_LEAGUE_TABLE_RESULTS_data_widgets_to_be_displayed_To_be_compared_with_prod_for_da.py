from json import JSONDecodeError
from voltron.utils.helpers import do_request
import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.adhoc06thFeb24
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.competitions
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.timeout(900)
@vtest
class Test_C66035615_To_verify_if_a_user_navigates_to_footballcompetitions_page_LEAGUE_TABLE_RESULTS_data_widgets_to_be_displayed_To_be_compared_with_prod_for_data_availability(
    BaseSportTest):
    """
    TR_ID: C66035615
    NAME: To verify if a user navigates to football competitions page LEAGUE TABLE and RESULTS data widgets to be displayed to be compared with prod for data availability
    DESCRIPTION: To verify if a user navigates to football>competitions page, LEAGUE TABLE & RESULTS data widgets to be displayed (To be compared with prod for data availability)
    PRECONDITIONS: 1) Load the Lads application
    PRECONDITIONS: 2)Navigate to the Football Landing page
    PRECONDITIONS: 3)Choose the 'Competitions' tab
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    show_less_button_name = vec.big_competitions.SHOW_LESS.upper()
    show_more_button_name = vec.SB.SHOW_ALL.upper()
    network_response_team_names = []

    # Getting result widget performance log from dev calls
    def get_result_widget_response(self, season_id, skip_number, limit_number):
        perflog = self.device.get_performance_log()
        expected_request_url = f'https://stats-centre.beta.coral.co.uk/api/season/{season_id}/matches/?skip={skip_number}&limit={limit_number}'

        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if expected_request_url in request_url:
                    break
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

        response = do_request(url=expected_request_url, method='GET')
        return response

    def verifying_league_table_and_results_widgets(self):
        if self.is_mobile:
            tabs_menu = self.site.competition_league.tabs_menu
            self.assertTrue(tabs_menu, msg='Tabs menu was not found')

            for tab_name, tab in tabs_menu.items_as_ordered_dict.items():
                self.assertIn(tab_name, vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values(),
                              msg='Market switcher tab is not present in the list')

            current_tab = tabs_menu.current
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}"')

            self.assertTrue(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict,
                            msg=f'No events found on "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}" tab')

            tabs_menu.click_button(vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings)
            current_tab = tabs_menu.current
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings}"')
            tabs_menu.click_button(vec.sb.COMPETITION_DETAILS_PAGE_TABS.results)
            current_tab = self.site.competition_league.tabs_menu.current
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.results,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.results}"')
        else:
            self.__class__.standings_widget = self.site.competition_league.standings_widget
            self.assertTrue(self.standings_widget.is_displayed(),
                            msg='Standings widget is not displayed')

            wait_for_haul(5)
            self.__class__.results_widget = self.site.competition_league.results_widget
            self.assertTrue(self.results_widget.is_displayed(), msg='Results widget is not displayed')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event and league
        """
        event = self.get_competition_with_results_and_standings_tabs(
            category_id=self.ob_config.football_config.category_id, raise_exceptions=True)
        self.__class__.season_id = int(event.season_id)
        sport_name = event.class_name.upper().split(" ")
        if sport_name[0] == vec.sb.FOOTBALL.upper():
            self.__class__.section_name = sport_name[1]
        else:
            self.__class__.section_name = sport_name[0]
        self.__class__.league = event.league_name

        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        self.__class__.league_table_label = vec.sb.LEAGUE_TABLE_LABEL.title() if self.brand == 'bma' else vec.sb.LEAGUE_TABLE_LABEL

    def test_001_navigate_to_competitions_page(self):
        """
        DESCRIPTION: Navigate to Competitions page
        EXPECTED: User should be navigated to Competitions page
        """
        self.navigate_to_page("sport/football")
        self.site.wait_content_state(state_name=vec.sb.FOOTBALL)

    def test_002_select_any_competition_from_popular_or_a_z(self):
        """
        DESCRIPTION: Select any Competition from "Popular" or "A-Z"
        EXPECTED: User is navigated to selected competition page
        """
        if self.is_mobile:
            self.site.football.tabs_menu.click_button(
                self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper())
            active_tab = self.site.football.tabs_menu.current
            self.assertEqual(active_tab, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper(),
                             msg=f'"{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()}" tab is not active, '
                                 f'active is "{active_tab}"')
            sections = self.site.football.tab_content.all_competitions_categories.get_items(name=self.section_name)
            self.assertTrue(sections, msg=f'Competitions page does not have any "{self.section_name}" section')
            section = sections.get(self.section_name)
            self.assertTrue(section, msg=f'"{self.section_name}" section not found in "{sections.keys()}"')
            if not section.is_expanded():
                section.expand()
            leagues = wait_for_result(lambda: section.get_items(name=self.league),
                                      name=f'"{self.section_name}" to expand for "{self.league}"', timeout=3)
            self.assertTrue(leagues, msg=f'No events are present for the league "{self.league}"')
            league = leagues.get(self.league)
            self.assertTrue(league, msg=f'Cannot find "{self.league}" on Competitions page')
            league.click()
            self.site.wait_content_state('CompetitionLeaguePage')
        else:
            self.site.football.tabs_menu.click_button(
                self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper())
            active_tab = self.site.football.tabs_menu.current
            self.assertEqual(active_tab, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper(),
                             msg=f'"{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()}" tab is not active, '
                                 f'active is "{active_tab}"')

            sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No countries found')
            if self.section_name.title() not in sections:
                grouping_buttons = self.site.football.tab_content.grouping_buttons.items_as_ordered_dict
                self.assertTrue(grouping_buttons, msg='No grouping buttons found')
                grouping_buttons[vec.sb_desktop.COMPETITIONS_SPORTS].click()

                sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(sections, msg='No countries found')
            if self.section_name not in ['USA', 'UEFA Club Competitions']:
                section_name = self.section_name if self.brand == 'bma' else self.section_name.title()
            else:
                section_name = self.section_name
            section = sections.get(section_name)
            self.assertTrue(section, msg=f'Section with name "{section_name}" is not found in "{sections.keys()}"')
            section.expand()
            leagues = wait_for_result(lambda: section.get_items(name=self.league),
                                      name=f'"{self.section_name}" to expand for "{self.league}"', timeout=3)
            self.assertTrue(leagues, msg=f'No events are present for the league "{self.league}"')
            league = leagues.get(self.league)
            self.assertTrue(league, msg=f'Cannot find "{self.league}" on Competitions page')
            league.click()
            self.site.wait_content_state('CompetitionLeaguePage')

    def test_003_verify_league_table_amp_results(self):
        """
        DESCRIPTION: Verify LEAGUE TABLE &amp; RESULTS
        EXPECTED: LEAGUE TABLE &amp; RESULTS should be displayed
        """
        self.verifying_league_table_and_results_widgets()

    def test_004_log_in_to_the_application_and_verify_league_table_amp_results(self):
        """
        DESCRIPTION: Log in to the application and verify LEAGUE TABLE &amp; RESULTS
        EXPECTED: LEAGUE TABLE &amp; RESULTS should be displayed in logged in state
        """
        self.site.login()
        if self.is_mobile:
            self.site.competition_league.tabs_menu.click_button(vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches)

        self.verifying_league_table_and_results_widgets()
        # getting team B names from performance logs
        first_response = list(self.get_result_widget_response(season_id=self.season_id, skip_number=0, limit_number=4))
        for i in range(0, len(first_response) - 1):
            team_name = first_response[i]['teamB']['name']
            self.network_response_team_names.append(team_name)

    def test_005_click_on_league_table(self):
        """
        DESCRIPTION: Click on "League table"
        EXPECTED: "League table" tab gets collapsed and chevron down icon is displayed
        """
        # verifying League table tab
        if not self.is_mobile:
            self.standings_widget.collapse()
            self.assertTrue(self.standings_widget.chevron_arrow.is_displayed(), msg='Chevron arrow is not displayed')
            self.standings_widget.expand()

            self.assertEqual(self.standings_widget.header_label, self.league_table_label,
                             msg=f'Label "{self.standings_widget.header_label}" '
                                 f'is not the same as expected "{self.league_table_label}"')

            self.assertTrue(self.standings_widget.season_name, msg='Season name is not displayed')

    def test_006_click_on_chevron_down_icon_on_league_table(self):
        """
        DESCRIPTION: Click on chevron down icon on League table
        EXPECTED: "League table" tab gets Expanded and chevron icon is not displayed
        """
        # Covered in step 5

    def test_007_click_on_show_all_in_league_table(self):
        """
        DESCRIPTION: Click on "Show All" in League table
        EXPECTED: Full data is displayed in League table
        """
        # Verifying League table show all link
        if not self.is_mobile:
            self.assertTrue(self.standings_widget.show_button.is_displayed(), msg='Show button is not displayed')
            self.standings_widget.show_button.click()
            result = wait_for_result(lambda: self.standings_widget.show_button.name == self.show_less_button_name,
                                     name='Show less button to be shown',
                                     timeout=2)
            self.assertTrue(result, msg='"Show less" button is not shown')

    def test_008_click_on_show_less_in_league_table(self):
        """
        DESCRIPTION: Click on "Show Less" in League table
        EXPECTED: Top 5 teams data is displayed in League table
        """
        # Verifying league table show less link
        if not self.is_mobile:
            self.standings_widget.show_button.click()
            result = wait_for_result(lambda: self.standings_widget.show_button.name == self.show_more_button_name,
                                     name='Show less button to be shown',
                                     timeout=2)
            self.assertTrue(result, msg='"Show all" button is not shown')

    def test_009_navigate_to_other_tabs_displayed_under_season_title_and_repeat__3_to_6(self):
        """
        DESCRIPTION: Navigate to other tabs displayed under Season title and repeat # 3 to 6
        EXPECTED: 
        """
        # Covered in above step

    def test_010_click_on_results_(self):
        """
        DESCRIPTION: Click on "RESULTS "
        EXPECTED: "RESULTS" tab gets collapsed and chevron down icon is displayed
        """
        if not self.is_mobile:
            self.results_widget.scroll_to()
            self.assertTrue(self.results_widget.header_label, msg="'Results'text is not displayed")
            self.assertTrue(self.results_widget.collapse, msg="'Results' widget is not collapsible")
        else:
            result_widget_sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
            for section_name, section in list(result_widget_sections.items()):
                if not section.is_expanded():
                    section.expand()

    def test_011_click_on_chevron_down_icon_on_league_table(self):
        """
        DESCRIPTION: Click on chevron down icon on League table
        EXPECTED: "RESULTS" tab gets Expanded and chevron icon is not displayed
        """
        if not self.is_mobile:
            self.assertTrue(self.results_widget.expand, msg="'Results' widget is not expandable")

    def test_012_click_on_show_more_in_results(self):
        """
        DESCRIPTION: Click on "Show More" in Results
        EXPECTED: Additional results data is displayed in Results
        """
        if not self.is_mobile:
            if self.results_widget.show_button:
                self.results_widget.show_button.click()
                second_response = self.get_result_widget_response(season_id=self.season_id, skip_number=3,
                                                                  limit_number=9)
                # getting team names from performance log
                for i in range(0, len(second_response) - 1):
                    team_name = second_response[i]['teamB']['name']
                    self.network_response_team_names.append(team_name)

    def test_013_click_on_show_more_in_results_again(self):
        """
        DESCRIPTION: Click on "Show More" in Results again
        EXPECTED: More past results are displayed
        """
        if not self.is_mobile:
            if self.results_widget.show_button:
                self.results_widget.show_button.click()
                # getting team names from performance log
                third_response = list(
                    self.get_result_widget_response(season_id=self.season_id, skip_number=11, limit_number=9))
                for i in range(0, len(third_response)-1):
                    team_name = third_response[i]['teamB']['name']
                    self.network_response_team_names.append(team_name)
            # getting team names from Front End Result widget
            self.site.competition_league.results_widget.scroll_to()
            result = wait_for_result(lambda: len(self.network_response_team_names) == self.site.competition_league.results_widget.count_of_items,
                                     timeout=50)
            self.assertTrue(result, msg='Teams are not displayed')
            result_widgets = self.site.competition_league.results_widget.items_as_ordered_dict
            self.__class__.team_names_from_FE = []
            for result in list(result_widgets.keys()):
                team_name = result.split('\n')
                self.team_names_from_FE.append(team_name[-1])

    def test_014_then_open_dev_tools__gt_network__gtxhr_tab_gtskip0(self):
        """
        DESCRIPTION: Then open dev tools -&gt; Network -&gt;XHR tab-&gt;?skip=0
        EXPECTED: New Skip api log is triggered for every click on "Show more"
        """
        # covered in above step

    def test_015_compare_data_of_api_and_fe(self):
        """
        DESCRIPTION: Compare data of API and FE
        EXPECTED: Results data of API should match with FE
        """
        # compare FE team names and Performance log team names
        if not self.is_mobile:
            self.assertListEqual(sorted(list(set(self.network_response_team_names))), sorted(list(set(self.network_response_team_names))),
                                 msg=f'Network call team names are:{sorted(list(set(self.network_response_team_names)))} are not equal to FE team names are:{sorted(list(set(self.network_response_team_names)))}')
        # in mobile mode we have different view of result widget, getting team names from Front End
        else:
            result_sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
            expected_team_name_from_FE = []
            for section in list(result_sections.values()):
                if not section.is_expanded():
                    section.expand()
                teams_names = list(section.team_names)
                for i in range(len(teams_names)):
                    if i % 2 != 0:
                        expected_team_name_from_FE.append(teams_names[i].text)
            # getting team names from performance logs
            actual_teams_names_from_dev = []
            network_response = self.get_result_widget_response(season_id=self.season_id, skip_number=0, limit_number=8)
            for i in range(0, len(network_response) - 1):
                team_name = network_response[i]['teamB']['name']
                actual_teams_names_from_dev.append(team_name)
            # compare team names from FE and Performance logs
            self.assertListEqual(sorted(expected_team_name_from_FE), sorted(actual_teams_names_from_dev),
                                 msg=f'Network call team names are:{sorted(actual_teams_names_from_dev)} are not equal to FE team names are:{sorted(expected_team_name_from_FE)}')

    def test_016_refresh_the_application(self):
        """
        DESCRIPTION: Refresh the application
        EXPECTED: "RESULTS" tab should display results of 3 events by default
        """
        self.device.refresh_page()

    def test_017_navigate_to_competitions_page_amp_select_any_competition_which_has_multiple_seasons_data(self):
        """
        DESCRIPTION: Navigate to Competitions page &amp; Select any Competition which has multiple seasons data
        EXPECTED: User is navigated to selected competition page
        """
        # covered in above steps

    def test_018_click_on_gt_symbol_under_league_table_title(self):
        """
        DESCRIPTION: Click on "&gt;" symbol under League Table title
        EXPECTED: Previous seasons points table to be displayed
        """
        # verifying League table < > arrows
        if self.is_mobile:
            self.site.competition_league.tabs_menu.click_button(vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings)
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
            current_league = self.site.competition_league.standings_widget.season_name
            if standings_widget.previous_arrow.is_displayed():
                self.site.competition_league.standings_widget.previous_arrow.click()
                wait_for_haul(2)
                previous_league = self.site.competition_league.standings_widget.season_name
                self.assertNotEqual(previous_league, current_league, msg='User is not navigating to previous league')
                self.site.competition_league.standings_widget.next_arrow.click()
                wait_for_haul(2)
                league_name = self.site.competition_league.standings_widget.season_name
                self.assertEqual(current_league, league_name, msg='user is not navigating to current league')
            else:
                self._logger.info(msg='there is no previous league table available')

    def test_019_then_open_dev_tools__gt_network__gtxhr_tab_gtstats_center_api(self):
        """
        DESCRIPTION: Then open dev tools -&gt; Network -&gt;XHR tab-&gt;stats-center api
        EXPECTED: Available seasons count is displayed in the api
        """
        # Covered in 17 and 18 steps

    def test_020_compare_the_available_seasons_count_from_stats_center_in_dev_tools_with_data_in_fe(self):
        """
        DESCRIPTION: Compare the available seasons count from (stats-center in dev tools) with data in FE
        EXPECTED: FE seasons count should match with information provided in API
        """
        # covered in above 17 and 18 steps

    def test_021_click_on_lt_symbol_under_league_table_title(self):
        """
        DESCRIPTION: Click on "&lt;" symbol under League Table title
        EXPECTED: Adjacent seasons points table to be displayed
        """
        # covered in step 18

    def test_022_click_on_lt_symbol_under_league_table_title_till_the_symbol_is_disappeared(self):
        """
        DESCRIPTION: Click on "&lt;" symbol under League Table title till the symbol is disappeared
        EXPECTED: User should be on the latest available season's League table points
        """
        # covered in step 18

    def test_023_verify_league_table_amp_results_when_event_is_in_pre_play(self):
        """
        DESCRIPTION: Verify LEAGUE TABLE &amp; RESULTS when event is in pre-play
        EXPECTED: LEAGUE TABLE: Should not consider the pre-play event in points table. &amp; RESULTS: Should be displayed as zero as event is in pre-play
        """
        # covered in above steps

    def test_024_verify_league_table_amp_results_when_event_is_in_in_play(self):
        """
        DESCRIPTION: Verify LEAGUE TABLE &amp; RESULTS when event is in in-play
        EXPECTED: LEAGUE TABLE: Should not consider the in-play event in points table. &amp; RESULTS: Should be displayed as zero as event is in in-play (As data job runs for every 24 hours and live feed is not available)
        """
        # covered in above steps

    def test_025_verify_league_table_amp_results_when_event_is_finished(self):
        """
        DESCRIPTION: Verify LEAGUE TABLE &amp; RESULTS when event is finished
        EXPECTED: No change from #4 ER (As data job runs for every 24 hours and live feed is not available)
        """
        # Covered in above steps

    def test_026_verify_league_table_amp_results_next_day(self):
        """
        DESCRIPTION: Verify LEAGUE TABLE &amp; RESULTS next day
        EXPECTED: Updated LEAGUE TABLE &amp; RESULTS should be displayed.
        """
        # covered in above steps

    def test_027_verify_ui_of_league_table_amp_results(self):
        """
        DESCRIPTION: Verify UI of LEAGUE TABLE &amp; RESULTS
        EXPECTED: UI of LEAGUE TABLE &amp; RESULTS should match with Prod
        """
        # covered in above steps

    def test_028_navigate_to_big_competitions_amp_select_results_tab(self):
        """
        DESCRIPTION: Navigate to Big competitions &amp; select Results tab
        EXPECTED: UI of LEAGUE TABLE &amp; RESULTS should match with Prod
        """
        # Covered in above steps

    def test_029_navigate_to_competition_which_has_multiple_tabs_in_league_table_example_uefa_champions_league_and_verify_data_in_all_tabs(
            self):
        """
        DESCRIPTION: Navigate to competition which has multiple tabs in LEAGUE TABLE. Example: UEFA-champions-league and verify data in all tabs
        EXPECTED: LEAGUE TABLE should display different tabs with data
        """
        # Covered in above steps

    def test_030_verify_data_in_different_tabs_in_league_table_for_various_competitions(self):
        """
        DESCRIPTION: Verify data in different tabs in LEAGUE TABLE for various competitions
        EXPECTED: LEAGUE TABLE should display different tabs with data for various competitions
        """
        # covered in above steps
