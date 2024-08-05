import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod // cannot create events for double chance market
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28532_Verify_selection_data_and_placing_a_bet_on_Double_Chance_market(BaseBetSlipTest):
    """
    TR_ID: C28532
    NAME: Verify selection data and placing a bet on Double Chance market
    DESCRIPTION: This test case verifies selection data and bet placement on Double Chance '90 mins / 1st Half / 2nd Half'  markets
    PRECONDITIONS: Football events with Double Chance '90 mins / 1st Half / 2nd Half' markets (name='Double Chance', name="Half-Time Double Chance"/"Half-Time Double Chance", name="Second-Half Double Chance")
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Half-Time Double Chance"
    PRECONDITIONS: *   PROD: name="1st Half Double Chance"
    PRECONDITIONS: **Jira ticket: **BMA-4073
    """
    keep_browser_open = True
    markets = [('double_chance', {'cashout': True}),
               ('half_time_double_chance', {'cashout': True}),
               ('second_half_double_chance', {'cashout': True})]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Football events with Double Chance markets
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)
        self.__class__.eventID = event_params.event_id
        self.__class__.outcome_value = {}

        for markets in event_params.ss_response['event']['children']:
            if markets['market']['templateMarketName'] in ['Double Chance', 'Half-Time Double Chance',
                                                           'Second-Half Double Chance']:
                for outcomes in markets['market']['children']:
                    self.outcome_value.update({outcomes['outcome']['id']: outcomes['outcome']['name']})

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

    def test_003_go_to_double_chance_market_section(self):
        """
        DESCRIPTION: Go to Double Chance market section
        EXPECTED: Market section is expandable/collapsible and consists of '90 mins / 1st Half / 2nd Half' sections
        """
        self.assertIn(self.expected_market_sections.double_chance, self.markets.keys())
        self.__class__.double_chance_market = self.markets.get(self.expected_market_sections.double_chance)
        self.double_chance_market.collapse()
        self.assertFalse(self.double_chance_market.is_expanded(expected_result=False),
                         msg=f'Market: "{self.expected_market_sections.double_chance}" section was not collapsed')
        self.double_chance_market.expand()
        self.assertTrue(self.double_chance_market.is_expanded(),
                        msg=f'Market: "{self.expected_market_sections.double_chance}" section was not expanded')

    def test_004_verify_selection_section(self):
        """
        DESCRIPTION: Verify selection section
        EXPECTED: Selection section is displayed within '90 mins / 1st Half / 2nd Half' sections and contains the following:
        EXPECTED: *   outcomes names correspond to the SS attribute 'name's for appropriate 'outcome ID'
        EXPECTED: *   Price/odds buttons
        EXPECTED: *   If price is not available - corresponding price/odds button is not shown
        """
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

        btn_2nd_half = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.second_half)
        self.assertTrue(btn_2nd_half, msg=f'Grouping button "{vec.sb.HANDICAP_SWITCHERS.second_half}" not found')
        self.assertTrue(btn_2nd_half.is_displayed(),
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.second_half}" is not displayed')

        self.__class__.selections = self.double_chance_market.outcomes.items_as_ordered_dict
        self.assertTrue(self.selections,
                        msg=f'No one selection found in market section: '
                            f'"{self.expected_market_sections.draw_no_bet}"')

        for outcome_name, outcome in self.selections.items():
            self.assertTrue(outcome.bet_button.outcome_price_text,
                            msg=f'Selection: "{outcome_name}" bet button not displayed')

        for _, _ in market_grouping_buttons.items():
            for outcome_name, outcome in self.selections.items():
                self.assertIn(outcome_name, self.outcome_value.values(),
                              msg=f'"{outcome_name}" outcome is not in "{self.outcome_value.values()}"')

    def test_005_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: Selection name corresponds to '**name**' attribute on the outcome level for verified market
        """
        # covered in step 4

    def test_006_verify_priceodds_button_correspondence_to_verified_market(self):
        """
        DESCRIPTION: Verify Price/Odds button correspondence to verified market
        EXPECTED: *   Price/odds buttons in '**90 mins**' tab correspond to 'Double Chance' market data in SS response
        EXPECTED: *   Price/odds buttons in '**1st Half**' tab correspond to 'Half-Time Double Chance' market data in SS response
        EXPECTED: *   Price/odds buttons in '**2nd Half**' tab correspond to 'Second-Half Double Chance' market data in SS response
        """
        # covered in step 4

    def test_007_verify_data_of_priceodds_button_in_fractional_format(self, format=None):
        """
        DESCRIPTION: Verify data of Price/Odds button in fractional format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled button is displayed with price if outcome is suspended
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
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled button is displayed with price if outcome is suspended
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.test_002_go_to_event_details_page_of_football_event()
        self.__class__.double_chance_market = self.markets.get(self.expected_market_sections.double_chance)
        self.__class__.selections = self.double_chance_market.outcomes.items_as_ordered_dict
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

    def test_010_add_single_selection_to_betslip(self):
        """
        DESCRIPTION: Add single selection to Betslip
        EXPECTED: Bet indicator displays 1
        """
        if self.device_type == 'mobile':
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        self.verify_betslip_counter_change(expected_value=1)

    def test_011_go_to_betslip(self):
        """
        DESCRIPTION: Go to 'Betslip'
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
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event name (event **'name'** attribute)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fractional format or **'price Dec'** in decimal format)
        """
        event_name = self.stake.name
        self.assertEqual(event_name.upper(), self.outcome_name.upper(),
                         msg=f'Selection name "{event_name.upper()}" is not the same as expected "{self.outcome_name.upper()}"')
        market_name = self.stake.market_name
        self.assertEqual(market_name, self.expected_market_sections.double_chance.title(),
                         msg=f'Market name "{market_name}" is not the same as expected "{self.expected_market_sections.double_chance.title()}"')
        odds = self.stake.odds
        self.assertEquals(odds, self.outcome.bet_button.outcome_price_text,
                          msg=f'odd "{odds}" is not same as expected "{self.outcome.bet_button.outcome_price_text}"')

    def test_013_add_amount_to_bet_using_stake_field_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake field or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   **Est. Returns**(Coral)/ **Pot. Returns** (Ladbrokes)
        EXPECTED: *   **Total Stake**
        EXPECTED: *   **Estimated Returns**(Coral)/ **Potential Returns** (Ladbrokes)
        """
        self.stake.amount_form.input.value = self.bet_amount
        self.verify_estimated_returns(
            est_returns=float(self.get_betslip_content().total_estimate_returns),
            odds=self.stake.odds, bet_amount=self.bet_amount)

    def test_014_tapplace_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User balance is changed accordingly
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(expected_user_balance=self.balance - self.bet_amount)
