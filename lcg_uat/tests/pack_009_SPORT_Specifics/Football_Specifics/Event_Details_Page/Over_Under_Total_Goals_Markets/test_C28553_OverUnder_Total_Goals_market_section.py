import voltron.environments.constants as vec
import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.event_details
@pytest.mark.football
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C28553_OverUnder_Total_Goals_market_section(BaseSportTest):
    """
    TR_ID: C28553
    NAME: Over/Under Total Goals market section
    DESCRIPTION: Test verifies 'Over / Under Total Goals' market section
    PRECONDITIONS: Football event with over/under markets (Total Goals Over/Under, Over/Under First Half , Over/Under Second Half)
    """
    keep_browser_open = True

    markets = [('over_under_total_goals', {'cashout': True, 'over_under': 1}),
               ('over_under_total_goals', {'cashout': True, 'over_under': 2}),
               ('over_under_total_goals', {'cashout': True, 'over_under': 3}),
               ('over_under_total_goals', {'cashout': True, 'over_under': 4}),
               ('over_under_total_goals', {'cashout': True, 'over_under': 5}),
               ('over_under_first_half', {'cashout': True, 'over_under': 6}),
               ('over_under_second_half', {'cashout': True, 'over_under': 7})]

    expected_buttons_names = vec.sb.EXPECTED_OVER_UNDER_TOTAL_GOALS_BUTTONS

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Football event with over/under markets
        EXPECTED: Appropriate football event was created
        """
        event = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)
        self.__class__.eventID = event.event_id
        self.__class__.event_name = f'{event.team1} v {event.team2}'

    def test_001_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(event_id=self.eventID)

        self.__class__.markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(self.markets_tabs_list,
                        msg=f'No market tab found on event: "{self.event_name}" details page')
        markets_tabs = self.markets_tabs_list.items_as_ordered_dict
        self.verify_edp_market_tabs_order(markets_tabs.keys())
        current_tab = self.markets_tabs_list.current
        expected_market_tab = self.get_default_tab_name_on_sports_edp(event_id=self.eventID)
        self.assertEqual(current_tab, expected_market_tab,
                         msg=f'"{expected_market_tab}" is not active tab, active tab is "{current_tab}"')

    def test_002_go_to_overunder_total_goals_market_section(self):
        """
        DESCRIPTION: Go to 'Over/Under Total Goals' market section
        EXPECTED: *   Section is present on Event Details Page and titled ‘Over/Under Total Goals’
        EXPECTED: *   It is possible to collapse/expand section
        """
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='Markets list is not present')

        self.__class__.market_name = self.expected_market_sections.over_under_total_goals

        self.assertTrue(self.market_name in markets_list,
                        msg=f'"{self.market_name}" section is not present')

        self.__class__.over_under_section = markets_list.get(self.market_name)

        self.over_under_section.collapse()
        self.assertFalse(self.over_under_section.is_expanded(expected_result=False),
                         msg=f'"{self.market_name}" section is not collapsed')

        self.over_under_section.expand()
        self.assertTrue(self.over_under_section.is_expanded(),
                        msg=f'"{self.market_name}" section is not expanded')

    def test_003_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If one of markets (Total Goals Over/Under <figure afterward>, Over/Under First Half <figure afterward>, Over/Under Second Half <figure afterward>)
        has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        self.assertTrue(self.over_under_section.market_section_header.has_cash_out_mark(),
                        msg=f'Market "{self.over_under_section}" has no cashout label')

    def test_004_expand_overunder_total_goals_market_section(self):
        """
        DESCRIPTION: Expand 'Over/Under Total Goals' market section
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

        self.assertTrue(self.over_under_section.has_show_all_button, msg='"SHOW ALL" button is not present')

    def test_005_verify_overunder_markets_shown_for_90_mins(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '90 mins'
        EXPECTED: *   Only markets with attribute **name="Total Goals Over/Under <figure afterward>" **are present
        EXPECTED: *   If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        self.assertEquals(len(self.over_under_section.outcomes.items_as_ordered_dict), 4,
                          msg=f'4 items should be shown under "{self.expected_buttons_names[0]}"'
                              f' column of "{self.over_under_section}" market')

    def test_006_verify_overunder_markets_shown_for_1st_half(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '1st Half'
        EXPECTED: *   Only markets with attribute **name="Over/Under First Half <figure afterward>" **are present
        EXPECTED: *   If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        result = self.over_under_section.grouping_buttons.click_button(vec.sb.HANDICAP_SWITCHERS.first_half, timeout=5)
        self.assertTrue(result,
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.first_half}" button was not selected')
        self.assertEquals(len(self.over_under_section.outcomes.items_as_ordered_dict), 1,
                          msg=f'Only one item should be present under "{vec.sb.HANDICAP_SWITCHERS.first_half}"'
                              f' column of "{self.over_under_section}" market')

    def test_007_verify_overunder_markets_shown_for_2nd_half(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '2nd Half'
        EXPECTED: *   Only markets with attribute **name="Over/Under Second Half <figure afterward>" **are present
        EXPECTED: *   If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        result = self.over_under_section.grouping_buttons.click_button(vec.sb.HANDICAP_SWITCHERS.second_half, timeout=5)
        self.assertTrue(result,
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.second_half}" button was not selected')

        self.assertEquals(len(self.over_under_section.outcomes.items_as_ordered_dict), 1,
                          msg=f'Only one item should be present under "{vec.sb.HANDICAP_SWITCHERS.second_half}"'
                              f' column of "{self.over_under_section}" market')
