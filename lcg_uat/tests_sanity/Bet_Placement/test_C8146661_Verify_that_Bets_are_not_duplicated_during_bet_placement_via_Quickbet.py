import re
import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  - cannot trigger price change on prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@pytest.mark.bet_placement
@pytest.mark.mobile_only
@pytest.mark.login
@pytest.mark.safari
@vtest
class Test_C8146661_Verify_that_Bets_are_not_duplicated_during_bet_placement_via_Quickbet(BaseRacing, BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C8146661
    VOL_ID: C51748958
    NAME: Verify that Bets are not duplicated during bet placement via Quickbet
    DESCRIPTION: This test case verifies that Bets are not duplicated during bet placement via Quickbet.
    DESCRIPTION: Before the issue was fixed bet was doubled if to trigger any error message in Quick Bet and to close it without bet placement.
    DESCRIPTION: If to trigger 3/4/5 messages and to close Quickbet after each of them was triggered and to place bet successfully after this - bet was x3/x4/x5 appropriately.
    PRECONDITIONS: 1. User is logged in to app with positive balance
    PRECONDITIONS: 2. User added selection to the Quickbet
    PRECONDITIONS: 3. To verify info in WS please use request url: wss://remotebetslip-XXX.coralsports.prod.cloud.ladbrokescoral.com/quickbet/?EIO=3&transport=websocket where XXX - specifies environment that is used for testing
    """
    keep_browser_open = True
    device_name = 'Pixel 2 XL' if not tests.use_browser_stack else tests.default_pixel
    prices = {0: '1/2', 1: '1/3'}
    new_price = '1/3'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. User is logged in to app with positive balance
        PRECONDITIONS: 2. User added selection to the Quickbet
        """
        # create test event
        event = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices=self.prices)
        self.__class__.selection_ids = list(event.selection_ids.values())
        self.__class__.selection_names = list(event.selection_ids.keys())
        eventID = event.event_id
        self.__class__.event_name = f'{event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.market_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.market_name.replace('|', '')
        self._logger.info(f'*** Found event "{self.event_name}" with ID "{eventID}"')
        username = tests.settings.betplacement_user
        self.site.login(username=username)
        self.__class__.user_balance = self.site.header.user_balance
        self.navigate_to_edp(event_id=eventID, sport_name='horse-racing')
        self.add_selection_to_quick_bet(outcome_name=self.selection_names[0])

    def test_001_trigger_a_price_change_for_the_selection_in_quickbet(self):
        """
        DESCRIPTION: Trigger a price change for the selection in QuickBet
        EXPECTED: * The updated price is received in WS
        EXPECTED: * The message is displayed in Quickbet
        EXPECTED: ![](index.php?/attachments/get/58771163) ![](index.php?/attachments/get/59323425)
        """
        self.ob_config.change_price(selection_id=self.selection_ids[0], price=self.new_price)
        if not self.is_safari:
            price_update = self.wait_for_price_update_from_live_serv(selection_id=self.selection_ids[0],
                                                                     price=self.new_price)
            self.assertTrue(price_update,
                            msg=f'Price update for selection "{self.selection_names[0]}" with id "{self.selection_ids[0]}" '
                                f'is not received')

        timeout = 60 if not self.is_safari else 2
        wait_for_result(lambda: self.site.quick_bet_panel.info_panels_text[0],
                        name='Price change message to appear',
                        timeout=timeout)

        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        expected_message = vec.quickbet.PRICE_IS_CHANGED.format(old=self.prices[0], new=self.new_price)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')

    def test_002_click_on_the_x_button_to_close_quickbet(self):
        """
        DESCRIPTION: Click on the 'X' button to close QuickBet
        EXPECTED: The Quickbet is closed
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick bet not closed')

    def test_003_add_any_selection_to_quickbet(self):
        """
        DESCRIPTION: Add any selection to Quickbet
        EXPECTED: The selection is added to QuickBet and received in WS
        """
        counter_value = len(self.site.header.bet_slip_counter.counter_value)
        if counter_value > 0:
            self.site.header.bet_slip_counter.click()
            self.clear_betslip()
            self.device.go_back()
        self.add_selection_to_quick_bet(outcome_name=self.selection_names[1])
        if not self.is_safari:
            response_id = 31001
            request = wait_for_result(
                lambda: self.get_web_socket_response_by_id(response_id=response_id, delimiter='42'),
                name=f'WS message with code {response_id} to appear',
                timeout=15,
                poll_interval=1)
            self.assertTrue(request, msg=f'Response with frame ID #{response_id} not received')
            self._logger.debug(f'*** Request data "{request}" for "{response_id}"')

            web_socket_selection = request['data']['event']['markets'][0]['outcomes'][0]['name']
            self.assertEqual(web_socket_selection, self.selection_names[1],
                             msg=f'The selection received in web socket "{web_socket_selection}" is not equal to '
                                 f'added to QuickBet "{self.selection_names[1]}"')
        else:
            self._logger.warning('Cannot test the selection is added to QuickBet and received in WS on Safari browser')

    def test_004_enter_any_stake(self):
        """
        DESCRIPTION: Enter any stake
        EXPECTED: * The keyboard appears
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Total Stake', 'Estimated Returns' - Coral, 'Total Stake', * 'Potential Returns' - Ladbrokes are calculated
        EXPECTED: * The buttons 'Add to betslip' and 'Place bet' are active
        EXPECTED: * The 'Boost' button is active and can be boosted (if available)
        EXPECTED: Please note The keyboard doesn't appear when using 'Quick Stake' buttons
        """
        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.amount_form.input.click()
        if not self.is_safari:
            self.enter_value_using_keyboard(value=self.bet_amount, on_betslip=False)
            self.assertTrue(self.site.quick_bet_panel.keyboard.is_displayed(
                name='Quick Stake keyboard shown', expected_result=True, timeout=5),
                msg='Numeric keyboard is not shown')
        else:
            quick_bet.amount_form.enter_amount(value=self.bet_amount)

        self.assertEqual(quick_bet.amount_form.input.value, str(self.bet_amount),
                         msg=f'Actual amount "{quick_bet.amount_form.input.value}" does not match '
                             f'expected "{self.bet_amount}"')
        actual_est_returns = self.site.quick_bet_panel.selection.bet_summary.total_estimate_returns
        self.verify_estimated_returns(est_returns=float(actual_est_returns),
                                      odds=[self.prices[1]],
                                      bet_amount=self.bet_amount)
        actual_stake = self.site.quick_bet_panel.selection.bet_summary.total_stake
        self.assertEqual(actual_stake, f'{self.bet_amount:.2f}',
                         msg=f'Actual "Total Stake" value "{actual_stake}" != Expected "{self.bet_amount:.2f}"')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='The button "Add to betslip" is not active')
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(), msg='The button "Place bet" is not active')

    def test_005_click_on_the_place_bet_button(self):
        """
        DESCRIPTION: Click on the 'Place bet' button
        EXPECTED: The bet is placed successfully
        """
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        self.__class__.expected_user_balance = self.user_balance - self.bet_amount

    def test_006_verify_the_number_of_placebet_requests_in_ws(self):
        """
        DESCRIPTION: Verify the number of PlaceBet requests in WS
        EXPECTED: Only ONE PlaceBet request is sent in WS (30011)
        EXPECTED: ![](index.php?/attachments/get/58771188) ![](index.php?/attachments/get/59323428)
        """
        if not self.is_safari:
            responses = []
            response_id = 30011

            # Parse log with responses
            logs = self.device.get_performance_log()
            for log in list(reversed(logs)):
                try:
                    data_dict = log[1]['message']['message']['params']['response']['payloadData'].split('[')
                    if data_dict[0] == str(42):
                        request = re.findall(r"^(.+?),", data_dict[1])[0].strip('"')
                        if request == str(response_id):
                            responses.append(data_dict)
                except (KeyError, TypeError, IndexError):
                    continue
            self.assertEqual(len(responses), 1,
                             msg=f'More than one request is present in remote betslip websocket: "{responses}"')
        else:
            self._logger.warning('Cannot test the number of PlaceBet requests in WS on Safari browser')

    def test_007_verify_the_bet_receipt_and_the_correct_balance_update(self):
        """
        DESCRIPTION: Verify the bet receipt and the correct balance update
        EXPECTED: * Balance is decreased is equal to the last stake value
        EXPECTED: * Only one bet receipt is received (30012)
        EXPECTED: ![](index.php?/attachments/get/58771189) ![](index.php?/attachments/get/59323429)
        """
        bet_receipt = self.site.quick_bet_panel.bet_receipt
        self.assertEqual(bet_receipt.name, self.selection_names[1],
                         msg=f'Actual Outcome name: "{bet_receipt.name}" '
                             f'does not match expected: "{self.selection_names[1]}"')
        self.assertEqual(bet_receipt.event_market, self.market_name,
                         msg=f'Actual Market name" "{bet_receipt.event_market}" '
                             f'does not match expected: "{self.market_name}"')
        self.assertEqual(bet_receipt.event_name, self.event_name,
                         msg=f'Actual Event name: "{bet_receipt.event_name}" '
                             f'does not match expected: "{self.event_name}"')

        self.verify_user_balance(expected_user_balance=self.expected_user_balance)

        if not self.is_safari:
            responses = []
            response_id = 30012

            # Parse log with responses
            logs = self.device.get_performance_log()
            for log in list(reversed(logs)):
                try:
                    data_dict = log[1]['message']['message']['params']['response']['payloadData'].split('[')
                    if data_dict[0] == str(42):
                        request = re.findall(r"^(.+?),", data_dict[1])[0].strip('"')
                        if request == str(response_id):
                            responses.append(data_dict)
                except (KeyError, TypeError, IndexError):
                    continue
            self.assertEqual(len(responses), 1,
                             msg=f'More than one request is present in remote betslip websocket: "{responses}"')
        else:
            self._logger.warning('Cannot test the number of bet receipt requests received (30012) in WS on Safari browser')

    def test_008_click_on_the_x_button_to_close_quickbet(self):
        """
        DESCRIPTION: Click on the 'X' button to close QuickBet
        EXPECTED: The quickbet is closed
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')

    def test_009_navigate_to_my_bets___open_betscashout_tabs_to_verify_the_number_of_placed_bets(self):
        """
        DESCRIPTION: Navigate to 'My Bets' -> 'Open Bets'/'Cashout' tabs to verify the number of placed bets
        EXPECTED: Only one placed bet with appropriate stake value and selection details is displayed in Open Bets/Cashout
        """
        bet_duplicates = []
        self.site.open_my_bets_open_bets()
        self.device.refresh_page()
        self.site.wait_content_state_changed()
        bets = wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list.get_items(number=5),
                               name='Bets to be loaded',
                               timeout=15)
        self.assertTrue(bets, msg='No bets found on "Open Bets" page')

        for event in bets.keys():
            if self.event_name in event:
                bet_duplicates.append(self.event_name)
        self.assertEqual(len(bet_duplicates), 1, msg=f'There are duplicated bets in Open Bets: "{bet_duplicates}"')
