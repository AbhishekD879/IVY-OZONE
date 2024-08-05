import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C28554_Over_Under_Home_Away_Team_Goals_market_section(BaseSportTest):
    """
    TR_ID: C28554
    NAME: Over/Under <Home/Away Team> Goals market section
    DESCRIPTION: This test case verifies 'Over/Under <Home/Away Team> Goals' market section on Event Details Page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with 'Over/Under <Home/Away Team> Total Goals' markets (Over/Under <Home/Away Team> Total Goals <figure afterward>, Over/Under First Half <Home/Away Team> Total Goals <figure afterward>, Over/Under Second Half <Home/Away Team> Total Goals <figure afterward>)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: *   **<figure afterward> **- variable part of market name shown in format 'X.5' as an amount of goals (e.g. 0.5, 1.5, 2.5 etc)
    PRECONDITIONS: *   **<Home Team>** - name of the team that is shown first in the Event Name
    PRECONDITIONS: *   **<Away Team>** - name of the team that is shown second in the Event Name
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Total Goals Over/Under x.x"
    PRECONDITIONS: *   PROD: name="Over/Under Total Goals x.x"
    PRECONDITIONS: **Jira ticket: **BMA-3902
    """
    keep_browser_open = True
    markets = [('over_under_home_team_total_goals', {'cashout': True, 'over_under': 1}),
               ('over_under_away_team_total_goals', {'cashout': True, 'over_under': 1}),
               ('over_under_first_half_home_team_total_goals', {'cashout': True, 'over_under': 1}),
               ('over_under_first_half_away_team_total_goals', {'cashout': True, 'over_under': 1}),
               ('over_under_second_half_home_team_total_goals', {'cashout': True, 'over_under': 1}),
               ('over_under_second_half_away_team_total_goals', {'cashout': True, 'over_under': 1})]
    expected_buttons_names = vec.sb.EXPECTED_OVER_UNDER_TOTAL_GOALS_BUTTONS

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Football event with over/under markets
        EXPECTED: Appropriate football event was created
        """
        event = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)
        self.__class__.eventID = event.event_id
        self.__class__.event_name = f'{event.team1} v {event.team2}'
        if self.brand == 'bma':
            if self.device_type == 'mobile':
                self.__class__.market_name = [f'Over/Under Goals {event.team1}'.upper(), f'Over/Under Goals {event.team2}'.upper()]
            else:
                self.__class__.market_name = [f'Over/Under Goals {event.team1}'.title(), f'Over/Under Goals {event.team2}'.title()]
        else:
            self.__class__.market_name = [f'Over/Under Goals {event.team1}'.title().replace('Auto Test', 'Auto test'),
                                          f'Over/Under Goals {event.team2}'.title().replace('Auto Test', 'Auto test')]

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('homepage')

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(event_id=self.eventID)
        markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(markets_tabs_list,
                        msg='No market tab found on event: "%s" details page' % self.event_name)
        markets_tabs_list.open_tab(vec.siteserve.EXPECTED_MARKET_TABS.all_markets)

    def test_003_go_to_overunder_home_team_goals_market_section(self):
        """
        DESCRIPTION: Go to 'Over/Under <Home Team> Goals' market section
        EXPECTED: *   Section is present on Event Details Page and titled ‘Over/Under <Home Team> Goals’
        EXPECTED: *   It is possible to collapse/expand section
        """
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='Markets list is not present')
        self.assertTrue(self.market_name[0] in markets_list,
                        msg=f'"{self.market_name[0]}" section is not present')

        self.__class__.over_under_section = markets_list.get(self.market_name[0])

        if not self.over_under_section.is_expanded():
            sleep(2)
            self.over_under_section.expand()
        self.assertTrue(self.over_under_section.is_expanded(),
                        msg=f'"{self.over_under_section}" section is not expanded')

    def test_004_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If one of markets (Over/Under <Home/Away Team> Total Goals <figure afterward>, Over/Under First Half <Home/Away Team> Total Goals <figure afterward>, Over/Under Second Half <Home/Away Team> Total Goals <figure afterward>) has cashoutAvail="Y" then label 'Cash Out' should be displayed next to market section name
        """
        self.assertTrue(self.over_under_section.market_section_header.has_cash_out_mark(),
                        msg=f'Market "{self.over_under_section}" has no cashout label')

    def test_005_expand_overunder_home_team_goals_market_section(self):
        """
        DESCRIPTION: Expand 'Over/Under <Home Team> Goals' market section
        EXPECTED: Section consists of:
        EXPECTED: *   Three buttons: '90 mins' (selected by default), '1st Half', '2nd Half'
        EXPECTED: *   'Total Goals' column with market names
        EXPECTED: *   'Over' and 'Under' columns with price/odds buttons
        EXPECTED: *   First four markets shown by default
        EXPECTED: *   'Show All' button (if more than 4 markets are available)
        """
        market_grouping_buttons = self.over_under_section.grouping_buttons.items_as_ordered_dict
        self.__class__.btn_90_min = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.ninety_mins)
        actual_buttons_names = [vec.sb.HANDICAP_SWITCHERS.ninety_mins, vec.sb.HANDICAP_SWITCHERS.first_half,
                                vec.sb.HANDICAP_SWITCHERS.second_half]
        self.assertEquals(actual_buttons_names, self.expected_buttons_names,
                          msg=f'Actual buttons names for "{self.over_under_section}" section: "{actual_buttons_names}" '
                              f'is not same as expected: "{self.expected_buttons_names}"')

        self.assertTrue(self.btn_90_min.is_selected(),
                        msg=f'"{self.expected_buttons_names[0]}" button is not selected by default')
        actual_columns = self.over_under_section.outcomes_table.columns
        expected_columns = vec.sb.EXPECTED_OVER_UNDER_TOTAL_GOALS_COLUMNS_DESKTOP if self.brand == 'ladbrokes' and self.device_type == 'desktop' else vec.sb.EXPECTED_OVER_UNDER_TOTAL_GOALS_COLUMNS
        self.assertEquals(actual_columns, expected_columns,
                          msg=f'Incorrect table tabs. Actual: "{actual_columns}", '
                              f'Expected: "{expected_columns}"')
        if len(self.over_under_section.outcomes.items_as_ordered_dict) == 4:
            self.assertTrue(self.over_under_section.has_show_all_button, msg='"SHOW ALL" button is not present')

    def test_006_verify_overunder_markets_shown_for_90_mins(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '90 mins'
        EXPECTED: *   Only markets with attribute **name="Over/Under <Home Team> Total Goals <figure afterward>" **are present
        EXPECTED: *   If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        self.assertEquals(len(self.over_under_section.outcomes.items_as_ordered_dict), 1,
                          msg=f'1 items should be shown under "{self.expected_buttons_names[0]}"'
                              f' column of "{self.over_under_section}" market')

    def test_007_verify_overunder_markets_shown_for_1st_half(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '1st Half'
        EXPECTED: *   Only markets with attribute **name="Over/Under First Half <Home Team> Total Goals <figure afterward>" **are present
        EXPECTED: *   If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        result = self.over_under_section.grouping_buttons.click_button(vec.sb.HANDICAP_SWITCHERS.first_half, timeout=5)
        self.assertTrue(result,
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.first_half}" button was not selected')
        self.assertEquals(len(self.over_under_section.outcomes.items_as_ordered_dict), 1,
                          msg=f'1 items should be shown under "{self.expected_buttons_names[1]}"'
                              f' column of "{self.over_under_section}" market')

    def test_008_verify_overunder_markets_shown_for_2nd_half(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '2nd Half'
        EXPECTED: *   Only markets with attribute **name="Over/Under Second Half <HomeTeam> Total Goals <figure afterward>" **are present
        EXPECTED: *   If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        result = self.over_under_section.grouping_buttons.click_button(vec.sb.HANDICAP_SWITCHERS.second_half, timeout=5)
        self.assertTrue(result,
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.second_half}" button was not selected')

        self.assertEquals(len(self.over_under_section.outcomes.items_as_ordered_dict), 1,
                          msg=f'1 items should be shown under "{self.expected_buttons_names[2]}"'
                              f' column of "{self.over_under_section}" market')

    def test_009_verify_overunder_home_team_goals_section_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify 'Over/Under <Home Team> goals' section in case of data absence
        EXPECTED: 'Over/Under <Home Team> goals' section is not shown if:
        EXPECTED: *   all markets that section consists of are absent
        EXPECTED: *   all markets that section consists of do not have any outcomes
        """
        # covered in above step

    def test_010_repeat_steps__4_9_for_overunderaway_teamgoals_market_section(self):
        """
        DESCRIPTION: Repeat steps № 4-9 for 'Over/Under **<Away Team> **Goals' market section
        EXPECTED:
        """
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='Markets list is not present')
        self.assertTrue(self.market_name[1] in markets_list,
                        msg=f'"{self.market_name[1]}" section is not present')

        self.__class__.over_under_section = markets_list.get(self.market_name[1])

        if not self.over_under_section.is_expanded():
            sleep(2)
            self.over_under_section.expand()
        self.assertTrue(self.over_under_section.is_expanded(),
                        msg=f'"{self.over_under_section}" section is not expanded')
        self.test_004_verify_cash_out_label_next_to_market_section_name()
        self.test_005_expand_overunder_home_team_goals_market_section()
        self.test_006_verify_overunder_markets_shown_for_90_mins()
        self.test_007_verify_overunder_markets_shown_for_1st_half()
        self.test_008_verify_overunder_markets_shown_for_2nd_half()
