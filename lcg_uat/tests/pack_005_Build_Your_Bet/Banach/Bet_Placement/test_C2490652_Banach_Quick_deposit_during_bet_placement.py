import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.banach
@pytest.mark.login
@pytest.mark.build_your_bet
@pytest.mark.build_your_bet_dashboard
@pytest.mark.user_journey_build_your_bet
@vtest
class Test_C2490652_Banach_Quick_deposit_during_bet_placement(BaseBanachTest, BaseBetSlipTest):
    """
    TR_ID: C2490652
    NAME: Banach. Quick deposit during bet placement
    DESCRIPTION: Test case describes Quick deposit during Banach bet placement
    DESCRIPTION: AUTOTEST [C2637448]
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: STEP 2: To be updated with correct messages and actual content after Redesign
    PRECONDITIONS: Check the following WS for details on adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: |||:Operation|:Banach code
    PRECONDITIONS: || Client adds selections to remote betslip | 50001
    PRECONDITIONS: || Response message for adding selections | 51001
    PRECONDITIONS: || Client sends Place bet message | 50011
    PRECONDITIONS: || Response message for Bet Placement | 51101
    PRECONDITIONS: || Client message to remove selections from betslip |30001
    PRECONDITIONS: || Response message when selections removed |30002
    PRECONDITIONS: * User has added at least two combinable selections to BYB **Coral**/Bet Builder **Ladbrokes** Dashboard
    PRECONDITIONS: * User has triggered Quick deposit menu and entered CVV and Amount
    """
    keep_browser_open = True
    proxy = None
    currency = '£'
    all_selection_names = []
    blocked_hosts = ['*spark-br.*']
    max_bet = 2.00
    bet_amount = 0.1
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Use request https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events
        """
        eventID = self.get_ob_event_with_byb_market()
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username, amount='5',
                                                                     card_number='5137651100600001',
                                                                     card_type='mastercard',
                                                                     expiry_month='12',
                                                                     expiry_year='2080',
                                                                     cvv='111'
                                                                     )
        self.site.login(username=username)
        self.site.wait_content_state('homepage')
        self.__class__.user_balance = self.site.header.user_balance
        self.navigate_to_edp(event_id=eventID)
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(
            self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg=f'Can not get market "{self.expected_market_sections.match_result}"')
        match_betting_selection_names = match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_names, msg='No one selection added to Dashboard')
        match_betting.add_to_betslip_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(), msg='BYB Dashboard panel is not shown')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)

        self.__class__.initial_counter += 1

        # Both Teams To Score selection
        both_teams_to_score_market = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)

        both_teams_to_score_names = both_teams_to_score_market.set_market_selection(selection_index=1, time=True)
        self.assertTrue(both_teams_to_score_names, msg='No one selection added to Dashboard')
        both_teams_to_score_market.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)

        self.__class__.initial_counter += 1
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)

        if self.site.sport_event_details.tab_content.dashboard_panel.has_price_not_available_message():
            self.assertFalse(
                self.site.sport_event_details.tab_content.dashboard_panel.price_not_available_message.is_displayed(
                    expected_result=False),
                msg=f'Message: "{vec.yourcall.PRICE_NOT_AVAILABLE}" displayed')

        self.__class__.summary_block = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary

        odds = self.summary_block.place_bet.value
        self.assertTrue(odds, msg='Can not get odds for given selections')

        self.assertEqual(self.summary_block.place_bet.text, vec.yourcall.PLACE_BET,
                         msg=f'Place bet button text: "{self.summary_block.place_bet.text}" '
                             f'is not the same as expected: "{vec.yourcall.PLACE_BET}"')

        self.summary_block.place_bet.scroll_to()
        self.summary_block.place_bet.click()
        # self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=False),
        #                  msg='Dashboard panel is displayed')
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='BYB Betslip not appears')

        byb_betslip_panel = self.site.byb_betslip_panel
        selections = byb_betslip_panel.selection.content.outcomes_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No one selection found in BYB betslip')
        self.__class__.all_selection_names = list(selections.keys())

        self.assertTrue(byb_betslip_panel.back_button.is_displayed(), msg='"BACK" button not displayed')
        self.assertTrue(byb_betslip_panel.place_bet.is_displayed(), msg='"PLACE BET" button not displayed')

        content = byb_betslip_panel.selection.content

        self.assertTrue(content.odds, msg='Odds value not found')
        self.assertTrue(content.amount_form.is_displayed(), msg='Amount input field not displayed')
        self.__class__.bet_amount = self.bet_amount + self.user_balance
        self.site.byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.bet_amount)

        make_deposit_button = self.site.quick_bet_panel.make_quick_deposit_button
        self.assertTrue(make_deposit_button.is_enabled(),
                        msg=f'"{make_deposit_button.name}" button is not enabled')
        self.assertEqual(make_deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual button name: "{make_deposit_button.name}" '
                             f'is not as expected: "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')
        make_deposit_button.click()
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(timeout=20),
                        msg=f'"Quick Deposit" panel is not displayed')
        # used sleep due to Quick deposit panel is taking time to load properly
        sleep(10)

    def test_001_tap_on_deposit_and_place_bet_button(self):
        """
        DESCRIPTION: Tap on DEPOSIT AND PLACE BET button
        EXPECTED: - On UI bet receipt is displayed
        EXPECTED: - User Balance is updated
        """
        quick_deposit = self.site.quick_bet_panel.quick_deposit_panel
        quick_deposit.stick_to_iframe()

        quick_deposit.cvv_2.click()
        if self.device_type == 'mobile':
            keyboard = quick_deposit.keyboard
            self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                            msg='Numeric keyboard is not shown')
            keyboard.enter_amount_using_keyboard(value=tests.settings.quick_deposit_card_cvv)
            keyboard.enter_amount_using_keyboard(value='enter')
        else:
            quick_deposit.cvv_2.input.value = tests.settings.quick_deposit_card_cvv
        deposit_button = quick_deposit.deposit_and_place_bet_button
        wait_for_result(lambda: quick_deposit.deposit_and_place_bet_button.name == vec.gvc.DEPOSIT_AND_PLACE_BTN,
                        name='Deposit & Place Bet button name',
                        timeout=20)
        self.assertTrue(deposit_button.is_enabled(), msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')
        deposit_button.click()
        quick_deposit.switch_to_main_page()

    def test_002_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify Bet Receipt
        EXPECTED: Correct values are displayed
        EXPECTED: - BET RECEIPT title
        EXPECTED: - 'Bet Placed Successfully' label and betting date and time
        EXPECTED: - Message **Your deposit was successful and your bet has been placed**
        EXPECTED: - Selections names
        EXPECTED: - Odds
        EXPECTED: - Bet ID
        EXPECTED: - Stake and Estimated Returns
        EXPECTED: From OX100.3 ( **LADBROKES ), OX 101.1 ( CORAL ) (fix version TBC):**
        EXPECTED: * Main Header: 'Bet receipt' title with 'X' button
        EXPECTED: * Sub header : Tick icon, 'Bet Placed Successfully' text, date & time stamp (in the next format: i.e. 19/09/2019, 14:57)
        EXPECTED: * Block of Bet Type Summary:
        EXPECTED: * Win Alerts Toggle (if enabled in CMS)
        EXPECTED: * bet type name: i.e. Bet Builder / Build Your Bet
        EXPECTED: * price of BYB selections bet : e.g @90/1
        EXPECTED: * Bet ID:( **Coral** )/Receipt No:( **Ladbrokes** ) e.g Bet ID: 0/17781521/0000041
        EXPECTED: * For each selection:
        EXPECTED: * selection name
        EXPECTED: * market
        EXPECTED: * (for Player bets: selection name and market in the format of X.X To Make X+ Passes)
        EXPECTED: * event name
        EXPECTED: Footer:
        EXPECTED: 'Total stake'( Coral ) / 'Stake for this bet' ( Ladbrokes )
        EXPECTED: 'Est. returns'( Coral ) / 'Potential returns' ( Ladbrokes )
        EXPECTED: Before OX100:
        EXPECTED: - Reuse Selection and Done buttons
        EXPECTED: After OX100:
        EXPECTED: - Close button ('X')
        """
        self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=25),
                        msg='Build Your Bet Receipt is not displayed')

        request = wait_for_result(lambda: self.get_web_socket_response_by_id(response_id=self.response_51101, delimiter='42'),
                                  name=f'WS message with code {self.response_51101} to appear',
                                  timeout=45,
                                  poll_interval=1)

        self.assertTrue(request, msg=f'Response with frame ID #{self.response_51101} not received')
        self._logger.debug(f'*** Request data "{request}" for "{self.response_51101}"')

        response_50011 = wait_for_result(
            lambda: self.get_web_socket_response_by_id(response_id=self.response_50011, delimiter='42'),
            name=f'WS message with code {self.response_50011} to appear',
            timeout=30,
            poll_interval=1)
        self.assertTrue(response_50011, msg=f'Response with frame ID #{self.response_50011} not received')
        self.assertEqual(response_50011.get('channel'), 'e',
                         msg=f'Channel: "e" is not present in "{self.response_50011}" request among "{response_50011}"')

        self.assertEqual(vec.quickbet.YOUR_CALL_BETRECEIPT, self.site.byb_bet_receipt_panel.header.title,
                         msg=f'Bet receipt header title does not equal "{vec.quickbet.YOUR_CALL_BETRECEIPT}" '
                             f'and is "{self.site.byb_bet_receipt_panel.header.title}" instead')

        bet_receipt_header = self.site.byb_bet_receipt_panel.bet_receipt.header
        self.assertEqual(bet_receipt_header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{bet_receipt_header.bet_placed_text}" is not equal to expected '
                             f'"{vec.betslip.SUCCESS_BET}"')
        self.assertTrue(bet_receipt_header.check_icon.is_displayed(), msg='"Check" icon is not displayed')
        self.assertRegex(bet_receipt_header.receipt_datetime, vec.regex.BET_DATA_TIME_FORMAT,
                         msg=f'Bet receipt data and time: "{bet_receipt_header.receipt_datetime}" '
                             f'do not match expected pattern: {vec.regex.BET_DATA_TIME_FORMAT}')

        bet_receipt_selection = self.site.byb_bet_receipt_panel.selection
        bet_receipt_content = bet_receipt_selection.content
        selections = bet_receipt_content.outcomes_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No one selection found in Build Your Bet receipt')

        selection_keys = list(selections.keys())
        expected_selection_keys = self.all_selection_names
        self.assertListEqual(selection_keys, expected_selection_keys,
                             msg=f'Incorrect market names.\nActual list: {selection_keys}'
                             f'\nExpected list: {expected_selection_keys}')
        self.assertTrue(bet_receipt_content.odds, msg='Odds value not found')
        self.assertEqual(bet_receipt_content.type_name.text, vec.yourcall.BUILD_YOUR_BET,
                         msg=f'Bet Type is: "{bet_receipt_content.type_name.text}", '
                             f'instead of "{vec.yourcall.BUILD_YOUR_BET}"')

        self.assertEqual(bet_receipt_content.bet_id_label, vec.betslip.BET_ID,
                         msg=f'Bet id label text is: "{bet_receipt_content.bet_id_label}" expecting "{vec.betslip.BET_ID}"')
        self.assertTrue(bet_receipt_content.bet_id_value, msg='Bet ID value not found')

        self.assertEqual(bet_receipt_selection.total_stake_label, vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT,
                         msg=f'Total Stake label text is: "{bet_receipt_selection.total_stake_label}", '
                             f'instead of "{vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT}"')
        self.assertIn(self.currency, bet_receipt_selection.total_stake)
        self.assertEqual(float(bet_receipt_selection.total_stake_value), self.bet_amount,
                         msg=f'Actual Total Stake value: "{float(bet_receipt_selection.total_stake_value)}" '
                             f'not match with expected: "{self.bet_amount}"')
        self.assertEqual(bet_receipt_selection.total_est_returns_label, vec.bet_history.TOTAL_RETURN,
                         msg=f'Total Est. Returns label text is: "{bet_receipt_selection.total_est_returns_label}", '
                             f'instead of "{vec.bet_history.TOTAL_RETURN}"')
        self.assertIn(self.currency, bet_receipt_selection.total_est_returns)
        self.assertTrue(bet_receipt_selection.total_est_returns_value, msg='Total Est. Returns value not found')
        self.assertTrue(self.site.byb_bet_receipt_panel.header.close_button, msg=f'"Close button" is not displayed on byb bet receipt panel')

    def test_003_tap_close_button(self):
        """
        DESCRIPTION: Tap 'Close' button
        EXPECTED: - Bet receipt is removed
        EXPECTED: - Selections are cleared in markets accordions
        """
        self.site.byb_bet_receipt_panel.header.close_button.click()
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=False),
                         msg='Build Your Bet Dashboard is still shown')
        expected_betslip_counter_value = 0
        self.verify_betslip_counter_change(expected_betslip_counter_value)
