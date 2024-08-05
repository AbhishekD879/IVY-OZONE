import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod //cannot create events for draw no bet
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28562_Verify_selection_data_and_placing_a_bet_on_Draw_No_Bet_markets(BaseBetSlipTest):
    """
    TR_ID: C28562
    NAME: Verify selection data and placing a bet on Draw No Bet markets
    DESCRIPTION: This test case verifies selection data and bet placement on Draw No Bet markets
    PRECONDITIONS: Football events with draw no bet markets (Draw No Bet, Half-Time Draw No Bet, Second-Half Draw No Bet)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: * XXX - the event ID
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: * TST2: name="Half-Time Draw No Bet"
    PRECONDITIONS: * PROD: name="1st Half Draw No Bet"
    PRECONDITIONS: **Jira ticket: **BMA-4072
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
        self.__class__.outcome_value = {}
        for markets in self.event_params.ss_response['event']['children']:
            if markets['market']['templateMarketName'] in ['Draw No Bet', 'Half-Time Draw No Bet',
                                                           'Second-Half Draw No Bet']:
                for outcomes in markets['market']['children']:
                    self.outcome_value.update({outcomes['outcome']['id']: outcomes['outcome']['name'].upper()})

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.login()
        self.__class__.balance = self.site.header.user_balance
        self.site.wait_content_state('Home')

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.__class__.markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No one market found on event details page')
        self.assertIn(self.expected_market_sections.draw_no_bet, self.markets.keys())

    def test_003_go_to_draw_no_bet_section(self):
        """
        DESCRIPTION: Go to 'Draw No Bet' section
        EXPECTED: Section is expandable/collapsible and displayed correctly
        """

        self.__class__.draw_no_bet_market = self.markets.get(self.expected_market_sections.draw_no_bet)
        self.draw_no_bet_market.collapse()
        self.assertFalse(self.draw_no_bet_market.is_expanded(expected_result=False),
                         msg=f'Market: "{self.expected_market_sections.draw_no_bet}" section was not collapsed')
        self.draw_no_bet_market.expand()
        self.assertTrue(self.draw_no_bet_market.is_expanded(),
                        msg=f'Market: "{self.expected_market_sections.draw_no_bet}" section was not expanded')

    def test_004_verify_selection_section(self):
        """
        DESCRIPTION: Verify selection section
        EXPECTED: Selection section is displayed within 'Draw No Bet' section and contains the following:
        EXPECTED: * Selection <Team> name
        EXPECTED: * Price/odds button
        EXPECTED: * If price is not available - corresponding price/odds button is not shown
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

        btn_2nd_half = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.second_half)
        self.assertTrue(btn_2nd_half, msg=f'Grouping button "{vec.sb.HANDICAP_SWITCHERS.second_half}" not found')
        self.assertTrue(btn_2nd_half.is_displayed(),
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.second_half}" is not displayed')

        self.__class__.selections = self.draw_no_bet_market.outcomes.items_as_ordered_dict
        self.assertTrue(self.selections,
                        msg=f'No one selection found in market section: '
                            f'"{self.expected_market_sections.draw_no_bet}"')

        for outcome_name, outcome in self.selections.items():
            self.assertTrue(outcome.bet_button.outcome_price_text,
                            msg=f'Selection: "{outcome_name}" bet button not displayed')

        for _, _ in market_grouping_buttons.items():
            for outcome_name, outcome in self.selections.items():
                self.assertIn(outcome_name.upper(), self.outcome_value.values(),
                              msg=f'"{outcome_name.upper()}" outcome is not in "{self.outcome_value.values()}"')

    def test_005_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: Selection name corresponds to '**name**' attribute on the outcome level for verified market
        """

        # covered in step 4

    def test_006_verify_priceodds_button_correspondence_to_verified_market(self):
        """
        DESCRIPTION: Verify Price/Odds button correspondence to verified market
        EXPECTED: * Price/odds buttons in '**90 mins**' filter correspond to 'Draw No Bet' market data in SS response
        EXPECTED: * Price/odds buttons in '**1st Half**' filter correspond to 'Half-Time Draw No Bet' market data in SS response
        EXPECTED: * Price/odds buttons in '**2nd Half**' filter correspond to 'Second-Half Draw No Bet' market data in SS response
        """
        # covered in step 4

    def test_007_verify_data_of_priceodds_button_in_fractional_format(self, format=None):
        """
        DESCRIPTION: Verify data of Price/Odds button in fractional format
        EXPECTED: * 'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: * Disabled **'S'** button is displayed instead of prices if outcome is suspended
        """
        for outcome_name, outcome in self.selections.items():
            if format == 'decimal':
                self.assertRegexpMatches(
                    outcome.bet_button.outcome_price_text,
                    self.decimal_pattern,
                    msg='odds are not displayed in fractional')
            else:
                self.assertRegexpMatches(
                    outcome.bet_button.outcome_price_text,
                    self.fractional_pattern,
                    msg='odds are not displayed in fractional')

    def test_008_verify_data_of_priceodds_button_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button in decimal format
        EXPECTED: * 'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: * Disabled **'S'** button is displayed instead of prices if outcome is suspended
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.test_002_go_to_event_details_page_of_football_event()
        self.__class__.draw_no_bet_market = self.markets.get(self.expected_market_sections.draw_no_bet)
        self.__class__.selections = self.draw_no_bet_market.outcomes.items_as_ordered_dict
        self.test_007_verify_data_of_priceodds_button_in_fractional_format(format='decimal')

    def test_009_selectunselect_same_priceodds_button(self):
        """
        DESCRIPTION: Select/unselect same Price/Odds button
        EXPECTED: Button is highlighted/unhighlighted respectively
        """
        self.__class__.outcome_name, self.__class__.outcome = list(self.selections.items())[0]
        self.assertFalse(self.outcome.bet_button.is_selected(expected_result=False),
                         msg=f'Bet button "{self.outcome_name}" is highlighted')
        self.outcome.bet_button.click()
        self.assertTrue(self.outcome.bet_button.is_selected(),
                        msg='Outcome button is not highlighted in green')

    def test_010_add_single_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add single selection to bet slip
        EXPECTED: Bet indicator displays 1.
        """
        if self.device_type == 'mobile':
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        self.verify_betslip_counter_change(expected_value=1)

    def test_011_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: The bet is present
        """
        self.site.open_betslip()
        self.site.close_all_dialogs(timeout=3)
        singles_section = self.get_betslip_sections().Singles
        _, self.__class__.stake = list(singles_section.items())[0]
        self.assertTrue(self.stake, msg=f'"{self.stake}" stake was not found in "{singles_section.keys()}"')

    def test_012_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Betslip:
        EXPECTED: 1. Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2. Market type (**'name'** attribute on the market level)
        EXPECTED: 3. Event start time and event name (**'startTime'** and event **'name'** attributes)
        EXPECTED: 4. Selection odds (**'PriceNum'/'PriceDen' **attributes in fraction format or **'price Dec'** in decimal format)
        """
        event_name = self.stake.name
        self.assertEqual(event_name.upper(), self.outcome_name.upper(),
                         msg=f'Selection name "{event_name.upper()}" is not the same as expected "{self.outcome_name.upper()}"')
        market_name = self.stake.market_name
        self.assertEqual(market_name, self.expected_market_sections.draw_no_bet.title(),
                         msg=f'Market name "{market_name}" is not the same as expected "{self.expected_market_sections.draw_no_bet.title()}"')
        odds = self.stake.odds
        self.assertEquals(odds, self.outcome.bet_button.outcome_price_text,
                          msg=f'odd "{odds}" is not same as expected "{self.outcome.bet_button.outcome_price_text}"')

    def test_013_add_amount_to_bet_using_stake_field_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake field or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: * **Estimated Returns**
        EXPECTED: * **Total Stake**
        EXPECTED: * **Total Est. Returns**
        """
        self.stake.amount_form.input.value = self.bet_amount
        self.verify_estimated_returns(
            est_returns=float(self.get_betslip_content().total_estimate_returns),
            odds=self.stake.odds, bet_amount=self.bet_amount)

    def test_014_tapbet_now_button(self):
        """
        DESCRIPTION: Tap **'Bet Now**' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User balance is changed accordingly
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(expected_user_balance=self.balance - self.bet_amount)
