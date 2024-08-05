import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cant created OB events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28557_Verify_ordering_of_markets_within_Over_Under_Total_Goals_sections(BaseSportTest):
    """
    TR_ID: C28557
    NAME: Verify ordering of markets within Over/Under Total Goals sections
    DESCRIPTION: This test case verifies ordering of markets within Over/Under Total Goals sections ('Over/Under Total Goals', 'Over/Under Total Goals <Home team>', 'Over/Under Total Goals <Away Team>').
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with over/under markets
    PRECONDITIONS: - Over/Under Total Goals: Total Goals Over/Under <figure afterward>, Over/Under First Half <figure afterward>, Over/Under Second Half <figure afterward>
    PRECONDITIONS: - Over/Under Total Goals <Home/Away Team>: Over/Under <Home/Away Team> Total Goals <figure afterward>, Over/Under First Half <Home/Away Team> Total Goals <figure afterward>, Over/Under Second Half <Home/Away Team> Total Goals <figure afterward>
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
    """
    keep_browser_open = True

    markets_over_under_total_goals =\
        [('over_under_total_goals', {'cashout': True, 'over_under': 1}),
         ('over_under_total_goals', {'cashout': True, 'over_under': 2}),
         ('over_under_total_goals', {'cashout': True, 'over_under': 3}),
         ('over_under_total_goals', {'cashout': True, 'over_under': 4}),
         ('over_under_total_goals', {'cashout': True, 'over_under': 5}),
         ('over_under_first_half', {'cashout': True, 'over_under': 6}),
         ('over_under_first_half', {'cashout': True, 'over_under': 7}),
         ('over_under_first_half', {'cashout': True, 'over_under': 8}),
         ('over_under_first_half', {'cashout': True, 'over_under': 9}),
         ('over_under_first_half', {'cashout': True, 'over_under': 10}),
         ('over_under_second_half', {'cashout': True, 'over_under': 11}),
         ('over_under_second_half', {'cashout': True, 'over_under': 12}),
         ('over_under_second_half', {'cashout': True, 'over_under': 13}),
         ('over_under_second_half', {'cashout': True, 'over_under': 14}),
         ('over_under_second_half', {'cashout': True, 'over_under': 15}),
         ('over_under_home_team_total_goals', {'cashout': True, 'over_under': 16}),
         ('over_under_first_half_home_team_total_goals', {'cashout': True, 'over_under': 17}),
         ('over_under_second_half_home_team_total_goals', {'cashout': True, 'over_under': 18}),
         ('over_under_away_team_total_goals', {'cashout': True, 'over_under': 19}),
         ('over_under_first_half_away_team_total_goals', {'cashout': True, 'over_under': 20}),
         ('over_under_second_half_away_team_total_goals', {'cashout': True, 'over_under': 21})]

    expected_buttons_names = vec.sb.EXPECTED_OVER_UNDER_TOTAL_GOALS_BUTTONS

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Football event with over/under markets
        EXPECTED: Appropriate football event was created
        """
        event_1 = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets_over_under_total_goals)
        self.__class__.eventID_1 = event_1.event_id
        self.__class__.event_name_1 = f'{event_1.team1} v {event_1.team2}'

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
        self.navigate_to_edp(event_id=self.eventID_1)
        markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(markets_tabs_list,
                        msg=f'No market tab found on event: "{self.event_name_1}" details page')
        markets_tabs_list.open_tab(vec.siteserve.EXPECTED_MARKET_TABS.all_markets)

    def test_003_go_to_overunder_total_goals_section(self):
        """
        DESCRIPTION: Go to 'Over/Under Total Goals' section
        EXPECTED: *   Section is expanded and shown correctly
        EXPECTED: *   '90 mins' button is selected by default
        EXPECTED: *   First four markets are shown by default within section
        """
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='Markets list is not present')
        self.__class__.market_name = self.expected_market_sections.over_under_total_goals
        self.assertTrue(self.market_name in markets_list,
                        msg=f'"{self.market_name}" section is not present')
        self.__class__.over_under_section = markets_list.get(self.market_name)

        self.__class__.market_name_1 = list(markets_list.keys())[2]
        self.__class__.over_under_section_home_team = markets_list.get(self.market_name_1)
        self.__class__.market_name_2 = list(markets_list.keys())[3]
        self.__class__.over_under_section_away_team = markets_list.get(self.market_name_2)

        self.over_under_section.collapse()
        self.assertFalse(self.over_under_section.is_expanded(expected_result=False),
                         msg=f'"{self.market_name}" section is not collapsed')

        self.over_under_section.expand()
        self.assertTrue(self.over_under_section.is_expanded(),
                        msg=f'"{self.market_name}" section is not expanded')

        self.__class__.market_grouping_buttons = self.over_under_section.grouping_buttons.items_as_ordered_dict
        btn_90_min = self.market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.ninety_mins)
        self.__class__.actual_buttons_names = [vec.sb.HANDICAP_SWITCHERS.ninety_mins, vec.sb.HANDICAP_SWITCHERS.first_half,
                                               vec.sb.HANDICAP_SWITCHERS.second_half]
        self.assertEquals(self.actual_buttons_names, self.expected_buttons_names,
                          msg=f'Actual buttons names for "{self.over_under_section}" section: "{self.actual_buttons_names}" '
                              f'is not same as expected: "{self.expected_buttons_names}"')

        self.assertTrue(btn_90_min.is_selected(),
                        msg=f'"{self.expected_buttons_names[0]}" button is not selected by default')
        actual_columns = self.over_under_section.outcomes_table.columns
        self.__class__.expected_columns = vec.sb.EXPECTED_OVER_UNDER_TOTAL_GOALS_COLUMNS_DESKTOP if self.brand == 'ladbrokes' and self.device_type == 'desktop' else vec.sb.EXPECTED_OVER_UNDER_TOTAL_GOALS_COLUMNS
        self.assertEquals(actual_columns, self.expected_columns,
                          msg=f'Incorrect table tabs. Actual: "{actual_columns}", '
                          f'Expected: "{self.expected_columns}"')
        self.assertTrue(self.over_under_section.has_show_all_button, msg='"SHOW ALL" button is not present')

    def test_004_clicktap_show_all_button(self):
        """
        DESCRIPTION: Click/Tap 'Show all' button
        EXPECTED: *   All available markets for selected button (option) are shown
        EXPECTED: *   Button is changed to 'Show less'
        """
        self.over_under_section.show_all_button.click()
        self.assertTrue(self.market_grouping_buttons, msg='"Markets list" is not present')
        self.assertTrue(self.over_under_section.show_less_button, msg='"SHOW LESS" button is not present')

    def test_005_verify_markets_order_within_section(self):
        """
        DESCRIPTION: Verify Markets order within section
        EXPECTED: Markets are ordered from lowest to highest <figure afterward> value of verified markets (e.g. 0.5, 1.5, 2.5 etc)
        """
        market_order = self.over_under_section.outcomes_table.items_names
        self.assertEquals(market_order, sorted(market_order),
                          msg='Outcomes for home team results are not sorted by team score')

    def test_006_repeat_steps_4_5_when_1st_half_button_is_selected(self):
        """
        DESCRIPTION: Repeat steps №4-5 when '1st Half' button is selected
        """
        btn_first_half = self.market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.first_half)
        btn_first_half.click()
        self.assertTrue(btn_first_half.is_selected(),
                        msg=f'"{self.expected_buttons_names[1]}" button is not selected by default')
        self.test_005_verify_markets_order_within_section()

    def test_007_repeat_steps_4_5_when_2nd_half_button_is_selected(self):
        """
        DESCRIPTION: Repeat steps №4-5 when '2nd Half' button is selected
        EXPECTED:
        """
        btn_second_half = self.market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.second_half)
        btn_second_half.click()
        self.assertTrue(btn_second_half.is_selected(),
                        msg=f'"{self.expected_buttons_names[2]}" button is not selected by default')
        self.test_005_verify_markets_order_within_section()

    def test_008_repeat_steps_4_7_for_overunder_total_goals_home_team_section(self):
        """
        DESCRIPTION: Repeat steps №4-7 for 'Over/Under Total Goals <Home team> section
        """
        self.over_under_section.collapse()
        self.assertFalse(self.over_under_section.is_expanded(expected_result=False),
                         msg=f'"{self.market_name}" section is not collapsed')

        self.over_under_section_home_team.expand()
        self.assertTrue(self.over_under_section_home_team.is_expanded(),
                        msg=f'"{self.market_name_1}" section is not expanded')

        market_grouping_buttons = self.over_under_section_home_team.grouping_buttons.items_as_ordered_dict
        btn_90_min = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.ninety_mins)
        self.assertEquals(self.actual_buttons_names, self.expected_buttons_names,
                          msg=f'Actual buttons names for "{self.over_under_section}" section: "{self.actual_buttons_names}" '
                              f'is not same as expected: "{self.expected_buttons_names}"')

        self.assertTrue(btn_90_min.is_selected(),
                        msg=f'"{self.expected_buttons_names[0]}" button is not selected by default')
        actual_columns = self.over_under_section_home_team.outcomes_table.columns
        self.assertEquals(actual_columns, self.expected_columns,
                          msg=f'Incorrect table tabs. Actual: "{actual_columns}", '
                          f'Expected: "{self.expected_columns}"')

        market_order = self.over_under_section_home_team.outcomes_table.items_names
        self.assertEquals(market_order, sorted(market_order),
                          msg='Outcomes for home team results are not sorted by team score')

        btn_first_half = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.first_half)
        btn_first_half.click()
        self.assertTrue(btn_first_half.is_selected(),
                        msg=f'"{self.expected_buttons_names[1]}" button is not selected by default')
        market_order = self.over_under_section_home_team.outcomes_table.items_names
        self.assertEquals(market_order, sorted(market_order),
                          msg='Outcomes for home team results are not sorted by team score')

        btn_second_half = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.second_half)
        btn_second_half.click()
        self.assertTrue(btn_second_half.is_selected(),
                        msg=f'"{self.expected_buttons_names[2]}" button is not selected by default')
        market_order = self.over_under_section_home_team.outcomes_table.items_names
        self.assertEquals(market_order, sorted(market_order),
                          msg='Outcomes for home team results are not sorted by team score')

    def test_009_repeat_steps_4_7_for_overunder_total_goals_away_team_section(self):
        """
        DESCRIPTION: Repeat steps №4-7 for 'Over/Under Total Goals <Away team> section
        EXPECTED:
        """
        self.over_under_section_home_team.collapse()
        self.assertFalse(self.over_under_section_home_team.is_expanded(expected_result=False),
                         msg=f'"{self.market_name_1}" section is not collapsed')

        self.over_under_section_away_team.expand()
        self.assertTrue(self.over_under_section_away_team.is_expanded(),
                        msg=f'"{self.market_name_1}" section is not expanded')

        market_grouping_buttons = self.over_under_section_away_team.grouping_buttons.items_as_ordered_dict
        btn_90_min = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.ninety_mins)
        self.assertEquals(self.actual_buttons_names, self.expected_buttons_names,
                          msg=f'Actual buttons names for "{self.over_under_section_away_team}" section: "{self.actual_buttons_names}" '
                              f'is not same as expected: "{self.expected_buttons_names}"')

        self.assertTrue(btn_90_min.is_selected(),
                        msg=f'"{self.expected_buttons_names[0]}" button is not selected by default')
        self.site.wait_content_state_changed(timeout=15)
        actual_columns = self.over_under_section_away_team.outcomes_table.columns
        self.assertEquals(actual_columns, self.expected_columns,
                          msg=f'Incorrect table tabs. Actual: "{actual_columns}", '
                          f'Expected: "{self.expected_columns}"')

        market_order = self.over_under_section_away_team.outcomes_table.items_names
        self.assertEquals(market_order, sorted(market_order),
                          msg='Outcomes for home team results are not sorted by team score')

        btn_first_half = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.first_half)
        btn_first_half.click()
        self.assertTrue(btn_first_half.is_selected(),
                        msg=f'"{self.expected_buttons_names[1]}" button is not selected by default')
        market_order = self.over_under_section_away_team.outcomes_table.items_names
        self.assertEquals(market_order, sorted(market_order),
                          msg='Outcomes for home team results are not sorted by team score')

        btn_second_half = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.second_half)
        btn_second_half.click()
        self.assertTrue(btn_second_half.is_selected(),
                        msg=f'"{self.expected_buttons_names[2]}" button is not selected by default')
        market_order = self.over_under_section_away_team.outcomes_table.items_names
        self.assertEquals(market_order, sorted(market_order),
                          msg='Outcomes for home team results are not sorted by team score')
