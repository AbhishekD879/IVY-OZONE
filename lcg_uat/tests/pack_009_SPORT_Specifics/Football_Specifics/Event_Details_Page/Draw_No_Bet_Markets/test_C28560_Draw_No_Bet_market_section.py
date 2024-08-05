import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod // cannot create events for draw no bet market
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28560_Draw_No_Bet_market_section(BaseSportTest):
    """
    TR_ID: C28560
    NAME: Draw No Bet market section
    DESCRIPTION: This test case verifies 'Draw No Bet' market section on Event Details Page
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with draw no bet markets (Draw No Bet, Half-Time Draw No Bet, Second-Half Draw No Bet)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Half-Time Draw No Bet"
    PRECONDITIONS: *   PROD: name="1st Half Draw No Bet"
    PRECONDITIONS: **Jira ticket: **BMA-4072
    """
    keep_browser_open = True
    markets = [('draw_no_bet', {'cashout': True}),
               ('half_time_draw_no_bet', {'cashout': True}),
               ('second_half_draw_no_bet', {'cashout': True})]

    def test_000_preconditions(self):
        """
              DESCRIPTION: Create test event
        """
        self.__class__.event_params = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)
        self.__class__.eventID = self.event_params.event_id
        if self.brand == 'ladbrokes':
            self.__class__.team1, self.__class__.team2 = self.event_params.team1.upper(), self.event_params.team2.upper()
        else:
            self.__class__.team1, self.__class__.team2 = self.event_params.team1, self.event_params.team2

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Home')

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_003_go_to_draw_no_bet_market_section(self):
        """
        DESCRIPTION: Go to 'Draw No Bet' market section
        EXPECTED: *   Section is present on Event Details Page and titled ‘Draw No Bet’
        EXPECTED: *   It is possible to collapse/expand section
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No one market found on event details page')
        self.assertIn(self.expected_market_sections.draw_no_bet, markets.keys())
        self.__class__.draw_no_bet_market = markets.get(self.expected_market_sections.draw_no_bet)
        self.draw_no_bet_market.collapse()
        self.assertFalse(self.draw_no_bet_market.is_expanded(expected_result=False),
                         msg=f'Market: "{self.expected_market_sections.draw_no_bet}" section was not collapsed')
        self.draw_no_bet_market.expand()
        self.assertTrue(self.draw_no_bet_market.is_expanded(),
                        msg=f'Market: "{self.expected_market_sections.draw_no_bet}" section was not expanded')

    def test_004_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If one of markets (Draw No Bet, Half-Time Draw No Bet, Second-Half Draw No Bet) has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        self.assertTrue(self.draw_no_bet_market.market_section_header.has_cash_out_mark(),
                        msg=f'Cash Out label not displayed next to market section name: '
                            f'"{self.expected_market_sections.draw_no_bet}"')

    def test_005_expand_draw_no_bet_market_section(self):
        """
        DESCRIPTION: Expand 'Draw No Bet' market section
        EXPECTED: Section consists of:
        EXPECTED: *   Three filters: '90 mins' (selected by default), '1st Half', '2nd Half'
        EXPECTED: *   <Home Team> and <Away Team> selections with corresponding price/odds buttons
        """
        market_grouping_buttons = self.draw_no_bet_market.grouping_buttons.items_as_ordered_dict
        self.assertTrue(market_grouping_buttons, msg=f'Grouping button not found for '
                                                     f'"{self.expected_market_sections.draw_no_bet}" market')
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

        self.__class__.selections = self.draw_no_bet_market.outcomes.items_as_ordered_dict
        self.assertTrue(self.selections,
                        msg=f'No one selection found in market section: '
                            f'"{self.expected_market_sections.draw_no_bet}"')
        home_or_draw_selection_name = f'{self.team1}'
        self.assertIn(home_or_draw_selection_name, self.selections.keys())
        self.assertTrue(self.selections[home_or_draw_selection_name].bet_button.is_displayed(),
                        msg=f'Selection: "{home_or_draw_selection_name}" bet button not displayed')
        away_or_draw_selection_name = f'{self.team2}'
        self.assertIn(away_or_draw_selection_name, self.selections.keys())
        self.assertTrue(self.selections[away_or_draw_selection_name].bet_button.is_displayed(),
                        msg=f'Selection: "{away_or_draw_selection_name}" bet button not displayed')

    def test_006_verify_market_shown_for_90_mins(self):
        """
        DESCRIPTION: Verify market shown for '90 mins'
        EXPECTED: Only market with attribute **name="Draw No Bet" **is present
        """
        draw_no_bet_selections = self.event_params.selection_ids.get('draw_no_bet')
        if self.brand == 'ladbrokes':
            draw_no_bet_selections = dict((k.upper(), v) for k, v in draw_no_bet_selections.items())
        self.assertListEqual(list(self.selections.keys()), list(draw_no_bet_selections.keys()),
                             msg=f'Actual displayed "90 mins" selections: {list(self.selections.keys())}, '
                                 f'expected: "{list(draw_no_bet_selections.keys())}"')

    def test_007_verify_market_shown_for_1st_half(self):
        """
        DESCRIPTION: Verify market shown for '1st Half'
        EXPECTED: Only market with attribute **name="Half-Time Draw No Bet" **is present
        """
        first_half_selections = self.event_params.selection_ids.get('half_time_draw_no_bet')
        if self.brand == 'ladbrokes':
            first_half_selections = dict((k.upper(), v) for k, v in first_half_selections.items())
        self.assertListEqual(list(self.selections.keys()), list(first_half_selections.keys()),
                             msg=f'Actual displayed "half_time_draw_no_bet" selections: {list(self.selections.keys())}, '
                                 f'expected: "{list(first_half_selections.keys())}"')

    def test_008_verify_market_shown_for_2nd_half(self):
        """
        DESCRIPTION: Verify market shown for '2nd Half'
        EXPECTED: Only market with attribute **name="Second-Half Draw No Bet"** is present
        """
        second_half_selections = self.event_params.selection_ids.get('second_half_draw_no_bet')
        if self.brand == 'ladbrokes':
            second_half_selections = dict((k.upper(), v) for k, v in second_half_selections.items())
        self.assertListEqual(list(self.selections.keys()), list(second_half_selections.keys()),
                             msg=f'Actual displayed "second_half_draw_no_bet" selections: {list(self.selections.keys())}, '
                                 f'expected: "{list(second_half_selections.keys())}"')

    def test_009_verify_selections_displaying_for_markets(self):
        """
        DESCRIPTION: Verify selections displaying for markets
        EXPECTED: *   <Home team> selection is shown first (on the left side) - outcome with attribute **outcomeMeaningMinorCode="H"**
        EXPECTED: *   <Away team> selection is shown second (on the right side) - outcome with attribute **outcomeMeaningMinorCode="A"**
        """
        # covered in 5-8 steps
