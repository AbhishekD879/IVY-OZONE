import pytest
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Event can not be created in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C28565_Verify_selection_data_and_placing_a_bet_on_1st_Half__2nd_Half_Result_markets(BaseBetSlipTest):
    """
    TR_ID: C28565
    NAME: Verify selection data and placing a bet on 1st Half / 2nd Half Result markets
    DESCRIPTION: This test case verifies selection data and bet placement on 1st Half / 2nd Half Result markets
    PRECONDITIONS: Football events with 1st Half / 2nd Half Result  markets (name="First-Half Result", name="Second-Half Result")
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First-Half Result"
    PRECONDITIONS: *   PROD: name="1st Half Result"
    PRECONDITIONS: **Jira ticket: **BMA-4074
    """
    keep_browser_open = True
    odds_price = []
    price_dec = []
    EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS = ['1ST HALF', '2ND HALF']

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Create a event
        """
        self.__class__.market_name = '1st Half / 2nd Half Result'
        markets_params = [('first_half_result', {'cashout': True}),
                          ('second_half_result', {'cashout': True})]
        event = self.ob_config.add_autotest_premier_league_football_event(markets=markets_params)
        self.__class__.eventID = event.event_id
        self.__class__.event_name = '%s v %s' % (event.team1, event.team2)
        for market in event.ss_response['event']['children']:
            self.__class__.market_names = ['First-Half Result', 'Second-Half Result']
            if market['market']['templateMarketName'] == self.market_names[0]:
                self.__class__.first_half_market = market['market']['children']
            elif market['market']['templateMarketName'] == self.market_names[1]:
                self.__class__.second_half_market = market['market']['children']

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('homepage')
        self.site.login()
        self.__class__.balance = self.site.header.user_balance

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(self.eventID, timeout=60)
        wait_for_result(lambda: self.site.wait_content_state(state_name='EventDetails'), timeout=120)
        markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(markets_tabs_list,
                        msg='No market tab found on event: "%s" details page' % self.event_name)
        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')

    def test_003_go_to_1st_half__2nd_half_result_section(self):
        """
        DESCRIPTION: Go to '1st Half / 2nd Half Result' section
        EXPECTED: Section is expandable/collapsible and displayed correctly
        """
        if self.brand == 'bma' and self.device_type == 'mobile':
            expected_market_name = self.market_name.upper()
        else:
            expected_market_name = self.market_name
        self.assertIn(expected_market_name, self.markets_list,
                      msg=f'"{expected_market_name}" section is not present')
        self.__class__.first_half_second_half = self.markets_list.get(expected_market_name)
        self.assertTrue(self.first_half_second_half,
                        msg=f'"{expected_market_name}" section is not found in "{self.markets_list.keys()}"')
        if not self.first_half_second_half.is_expanded():
            sleep(2)
            self.first_half_second_half.expand()
        self.assertTrue(self.first_half_second_half.is_expanded(),
                        msg=f'"{self.first_half_second_half}" section is not expanded')

    def test_004_verify_selection_section(self):
        """
        DESCRIPTION: Verify selection section
        EXPECTED: Selection section is displayed within '1st Half / 2nd Half Result' section and contains the following:
        EXPECTED: *   Selection <Team name>/<Draw>
        EXPECTED: *   Price/odds button
        EXPECTED: *   If price is not available - corresponding price/odds button is not shown
        """
        first_half_second_half = self.first_half_second_half.grouping_buttons.items_names
        self.assertEqual(first_half_second_half, self.EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS,
                         msg=f'Actual market headers "{first_half_second_half}" '
                             f'are not same as expected headers: "{self.EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS}"')
        btn_1st_half = self.first_half_second_half.grouping_buttons.items_as_ordered_dict.get(
            vec.sb.HANDICAP_SWITCHERS.first_half)
        self.assertTrue(btn_1st_half.is_selected(),
                        msg=f'"{self.EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS[0]}" button is not selected by default')
        switchers = self.first_half_second_half.grouping_buttons.items_as_ordered_dict
        for name, switcher in switchers.items():
            switcher.click()
            selections_list = self.first_half_second_half.outcomes.items
            self.assertEqual(len(selections_list), 3,
                             msg=f'Actual outcomes length: "{len(selections_list)}" is not same as '
                                 f'Expected length: "3"')
            self.__class__.selection_name = []
            self.__class__.selection_price = []
            for selection in range(len(selections_list)):
                self.selection_name.append(selections_list[selection].name)
                self.selection_price.append(selections_list[selection].output_price)
                self.assertTrue(self.selection_name, msg=f'selection name: "{self.selection_name}" is not displayed')
                self.__class__.selection = selections_list[selection].bet_button
                self.assertTrue(self.selection.is_displayed(),
                                msg=f'selection bet button: "{self.selection_name}" is not displayed')

    def test_005_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: Selection name corresponds to '**name**' attribute on the outcome level for verified market
        """
        self.__class__.expected_selection_name = []
        for i in self.second_half_market:
            self.expected_selection_name.append(i['outcome']['name'])
            price_num = i['outcome']['children'][0]['price']['priceNum']
            price_den = i['outcome']['children'][0]['price']['priceDen']
            self.odds_price.append(f'{price_num}/{price_den}')
            self.price_dec.append(i['outcome']['children'][0]['price']['priceDec'])
        self.assertEqual(self.selection_name, self.expected_selection_name,
                         msg=f'Actual selection name: "{self.selection_name}" is not same as '
                             f'Expected selection name: "{self.expected_selection_name}"')

    def test_006_verify_priceodds_button_correspondence_to_verified_market(self):
        """
        DESCRIPTION: Verify Price/Odds button correspondence to verified market
        EXPECTED: *   Price/odds buttons in '**1st Half Result**' tab correspond to 'First-Half Result' market data in SS response
        EXPECTED: *   Price/odds buttons in '**2nd Half Result**' tab correspond to 'Second-Half Result' market data in SS response
        EXPECTED: **Note: **Name differences could be present for different events and environments
        """
        # covered in step 4

    def test_007_verify_data_of_priceodds_button_in_fractional_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button in fractional format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if outcome is suspended
        """
        self.assertEqual(self.selection_price, self.odds_price,
                         msg=f'Actual odds price: "{self.selection_price}" is not same as '
                             f'Expected odds price: "{self.odds_price}"')

    def test_008_verify_data_of_priceodds_button_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if outcome is suspended
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.test_002_go_to_event_details_page_of_football_event()
        self.test_003_go_to_1st_half__2nd_half_result_section()
        self.test_004_verify_selection_section()
        self.assertEqual(self.selection_price, self.price_dec,
                         msg=f'Actual odds price: "{self.selection_price}" is not same as '
                             f'Expected odds price: "{self.price_dec}"')

    def test_009_selectunselect_same_priceodds_button(self):
        """
        DESCRIPTION: Select/unselect same Price/Odds button
        EXPECTED: Button is highlighted/unhighlighted respectively
        """
        self.selection.click()
        self.assertTrue(self.selection.is_selected(), msg=f'selection "{self.selection}" is not selected')

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
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event start time and event name (**'startTime'** and event **'name'** attributes)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fraction format or **'price Dec'** in decimal format)
        """
        event_name = self.stake.name
        self.assertEqual(event_name.upper(), self.selection_name[2],
                         msg=f'Selection name "{event_name.upper()}" is not the same as expected "{self.selection_name[2]}"')
        market_name = self.stake.market_name
        self.assertEqual(market_name, self.market_names[1],
                         msg=f'Actual Market name: "{market_name}" is not the same as'
                             f'Expected Market name: "{self.market_names[1]}"')
        odds = self.stake.odds
        self.assertEquals(odds, self.selection.outcome_price_text,
                          msg=f'odd "{odds}" is not same as expected "{self.selection.outcome_price_text}"')

    def test_013_add_amount_to_bet_using_stake_field_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake field or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   **Estimated Returns**
        EXPECTED: *   **Total Stake**
        EXPECTED: *   **Total Est. Returns**
        """
        self.stake.amount_form.input.value = self.bet_amount
        self.verify_estimated_returns(
            est_returns=float(self.get_betslip_content().total_estimate_returns),
            odds=self.stake.odds, bet_amount=self.bet_amount)

    def test_014_tapbet_now_button(self):
        """
        DESCRIPTION: Tap **'Bet Now**' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User balance is changed accordingly
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(expected_user_balance=self.balance - self.bet_amount)
