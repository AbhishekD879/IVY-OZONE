import voltron.environments.constants as vec
import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.markets
@pytest.mark.double_chance
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C28530_Double_Chance_market_section(BaseSportTest):
    """
    TR_ID: C28530
    NAME: Double Chance market section
    DESCRIPTION: This test case verifies Double Chance market section
    PRECONDITIONS: Football events with Double Chance markets:
    PRECONDITIONS:    * name="Double Chance",
    PRECONDITIONS:    * name="First-Half Double Chance,
    PRECONDITIONS:    * name="Second-Half Double Chance")
    PRECONDITIONS: Note: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS:    * TST2: name="Half-Time Double Chance"
    PRECONDITIONS:    * PROD: name="1st Half Double Chance"
    """
    keep_browser_open = True
    markets = [('double_chance', {'cashout': True}),
               ('half_time_double_chance', {'cashout': True}),
               ('second_half_double_chance', {'cashout': True})]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Football events with Double Chance markets
        """
        self.__class__.event_params = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)
        self.__class__.eventID = self.event_params.event_id
        self.__class__.team1, self.__class__.team2 = self.event_params.team1, self.event_params.team2

    def test_001_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_002_go_to_double_chance_market_section(self):
        """
        DESCRIPTION: Go to 'Double Chance' market section
        EXPECTED: Section is present on Event Details Page and titled 'Double Chance'
        EXPECTED: It is possible to collapse/expand section
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No one market found on event details page')
        self.assertIn(self.expected_market_sections.double_chance, markets.keys())
        self.__class__.double_chance_market = markets.get(self.expected_market_sections.double_chance)
        self.double_chance_market.collapse()
        self.assertFalse(self.double_chance_market.is_expanded(expected_result=False),
                         msg=f'Market: "{self.expected_market_sections.double_chance}" section was not collapsed')
        self.double_chance_market.expand()
        self.assertTrue(self.double_chance_market.is_expanded(),
                        msg=f'Market: "{self.expected_market_sections.double_chance}" section was not expanded')

    def test_003_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If one of Double Chance markets:
        EXPECTED: * Double Chance
        EXPECTED: * Half-Time Double Chance
        EXPECTED: * Second-Half Double Chance
        EXPECTED: has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        self.assertTrue(self.double_chance_market.market_section_header.has_cash_out_mark(),
                        msg=f'Cash Out label not displayed next to market section name: '
                            f'"{self.expected_market_sections.double_chance}"')

    def test_004_expand_double_chance_market_section(self):
        """
        DESCRIPTION: Expand 'Double Chance' market section
        EXPECTED: Section consists of:
        EXPECTED:  * Three buttons: '90 mins' (selected by default), '1st Half', '2nd Half'
        EXPECTED:  * <Home Team or Draw>, <Away Team or Draw>, <Home Team or Away Team> selections with corresponding price/odds buttons
        """
        # Section already expanded in step 2

        market_grouping_buttons = self.double_chance_market.grouping_buttons.items_as_ordered_dict
        self.assertTrue(market_grouping_buttons, msg=f'Grouping button not found for '
                                                     f'"{self.expected_market_sections.double_chance}" market')
        btn_90_min = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.ninety_mins)
        self.assertTrue(btn_90_min, msg=f'Grouping button "{vec.sb.HANDICAP_SWITCHERS.ninety_mins}" not found')
        self.assertTrue(btn_90_min.is_selected(),
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.ninety_mins}" is not selected by default')

        btn_1st_half = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.first_half)
        self.assertTrue(btn_1st_half, msg=f'Grouping button "{vec.sb.HANDICAP_SWITCHERS.first_half}" not found')
        self.assertTrue(btn_1st_half.is_displayed(),
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.first_half}" is not displayed')

        btn_2nd_half = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.first_half)
        self.assertTrue(btn_2nd_half, msg=f'Grouping button "{vec.sb.HANDICAP_SWITCHERS.second_half}" not found')
        self.assertTrue(btn_2nd_half.is_displayed(),
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.second_half}" is not displayed')

        self.__class__.selections = self.double_chance_market.outcomes.items_as_ordered_dict
        self.assertTrue(self.selections,
                        msg=f'No one selection found in market section: '
                            f'"{self.expected_market_sections.double_chance}"')
        home_or_draw_selection_name = f'{self.team1} or Draw'
        self.assertIn(home_or_draw_selection_name, self.selections.keys())
        self.assertTrue(self.selections[home_or_draw_selection_name].bet_button.is_displayed(),
                        msg=f'Selection: "{home_or_draw_selection_name}" bet button not displayed')
        away_or_draw_selection_name = f'{self.team2} or Draw'
        self.assertIn(away_or_draw_selection_name, self.selections.keys())
        self.assertTrue(self.selections[away_or_draw_selection_name].bet_button.is_displayed(),
                        msg=f'Selection: "{away_or_draw_selection_name}" bet button not displayed')
        home_or_away_selection_name = f'{self.team1} or {self.team2}'
        self.assertIn(home_or_away_selection_name, self.selections.keys())
        self.assertTrue(self.selections[home_or_away_selection_name].bet_button.is_displayed(),
                        msg=f'Selection: "{home_or_away_selection_name}" bet button not displayed')

    def test_005_verify_double_chance_market_shown_for_90_mins(self):
        """
        DESCRIPTION: Verify Double Chance market shown for '90 mins'
        EXPECTED: Only market with attribute **name="Double Chance" **is present
        EXPECTED: If market/outcomes within market are absent - nothing is shown within selected option
        """
        double_chance_selections = self.event_params.selection_ids.get('double_chance')
        self.assertListEqual(list(self.selections.keys()), list(double_chance_selections.keys()),
                             msg=f'Actual displayed "90 mins" selections: {list(self.selections.keys())}, '
                                 f'expected: "{list(double_chance_selections.keys())}"')

    def test_006_verify_double_chance_market_shown_for_1st_half(self):
        """
        DESCRIPTION: Verify Double Chance market shown for '1st Half'
        EXPECTED: Only market with attribute **name="First-Half Double Chance" **is present
        EXPECTED: If market/outcomes within market are absent - nothing is shown within selected option
        """
        result = self.double_chance_market.grouping_buttons.click_button(vec.sb.HANDICAP_SWITCHERS.first_half, timeout=3)
        self.assertTrue(result,
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.first_half}" button was not selected')
        selections = self.double_chance_market.outcomes.items_as_ordered_dict
        first_half_double_chance_selections = self.event_params.selection_ids.get('half_time_double_chance')
        self.assertListEqual(list(selections.keys()), list(first_half_double_chance_selections.keys()),
                             msg=f'Actual displayed "1st Half" selections: {list(selections.keys())}, '
                                 f'expected: "{list(first_half_double_chance_selections.keys())}"')

    def test_007_verify_double_chance_market_shown_for_2nd_half(self):
        """
        DESCRIPTION: Verify Double Chance market shown for '2nd Half'
        EXPECTED: Only market with attribute **name="Second-Half Double Chance" **is present
        EXPECTED: If market/outcomes within market are absent - nothing is shown within selected option
        """
        result = self.double_chance_market.grouping_buttons.click_button(vec.sb.HANDICAP_SWITCHERS.second_half)
        self.assertTrue(result,
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.second_half}" button was not selected')
        selections = self.double_chance_market.outcomes.items_as_ordered_dict
        second_half_double_chance_selections = self.event_params.selection_ids.get('second_half_double_chance')
        self.assertListEqual(list(selections.keys()), list(second_half_double_chance_selections.keys()),
                             msg=f'Actual displayed "2nd Half" selections: {list(selections.keys())}, '
                                 f'expected: "{list(second_half_double_chance_selections.keys())}"')

    def test_008_verify_selections_displaying_for_markets(self):
        """
        DESCRIPTION: Verify selections displaying for markets
        EXPECTED: selection is shown first - outcome with attribute **outcomeMeaningMinorCode="1"**
        EXPECTED: selection is shown second - outcome with attribute **outcomeMeaningMinorCode="2"**
        EXPECTED: selection is shown third - outcome with attribute **outcomeMeaningMinorCode="3"**
        """
        # Selections displaying for markets validations covered indirectly in steps 5-7
