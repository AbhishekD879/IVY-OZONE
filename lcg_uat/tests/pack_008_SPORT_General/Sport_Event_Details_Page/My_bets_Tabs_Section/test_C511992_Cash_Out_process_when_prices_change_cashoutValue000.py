import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result


# Applicable only for coral
@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C511992_Cash_Out_process_when_prices_change_cashoutValue000(BaseCashOutTest):
    """
    TR_ID: C511992
    NAME: Cash Out process when prices change (cashoutValue="0.00")
    DESCRIPTION: This test case verifies Cash Out process when prices change on 'My Bets' tab on Event Details page
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-24365 My Bets Improvement : CashOut: Redesign of main cashout CTA Partial Cashout] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24365
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: *   Open Dev tools -> Network tab -> XHR sorting type -> choose **getBetDetail?** / **getBetDetails?** request
    PRECONDITIONS: **Currently CASH OUT option is available on back-end for Football, Tennis, Darts, and Snooker (other sports will be added in future).**
    PRECONDITIONS: **From release XXX.XX:**
    PRECONDITIONS: - Open Dev Tools -> Network tab -> WS filter (cashout request)
    PRECONDITIONS: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: - initial bets data will be returned after establishing connection
    """
    keep_browser_open = True
    event_params = None
    bet_amount = 1
    correct_price = '4/1'
    incorrect_price = '400/1'
    expected_message = vec.bet_history.CASHOUT_BET.cashout_unavailable.bet_worth_nothing

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Login
        DESCRIPTION: Place bets
        """
        events = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        self.__class__.team1, team2 = [event.team1 for event in events]
        self.__class__.selection_ids = {event.team1: event.selection_ids[event.team1] for event in events}
        self.site.login()
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values()))
        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_bets_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets with available cash out
        """
        self.site.open_my_bets_cashout()

    def test_002_go_to_single_cash_out_bet_line(self):
        """
        DESCRIPTION: Go to **Single** Cash Out bet line
        """
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.single_bet = list(bets.values())[0]
        self.__class__.multiple_bet = list(bets.values())[1]
        self.assertTrue(self.single_bet, msg='Single Bet is not displayed')
        self.assertTrue(self.multiple_bet, msg='multiple Bet is not displayed')

    def test_003_trigger_price_change_in_openbet_ti_tool_for_current_selection_eg_change_price_from_41_to_4001(self):
        """
        DESCRIPTION: Trigger price change in Openbet TI tool for current selection (e.g change price from 4/1 to 400/1)
        EXPECTED: * Price is changed for selection
        EXPECTED: * **cashoutValue="0.00"** is received in **getBetDetail?** responce
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Price is changed for selection
        EXPECTED: * **cashoutValue="0.00"** is received in cashoutUpdate via WebSocket
        """
        self.ob_config.change_price(self.selection_ids[self.team1], self.incorrect_price)

    def test_004_verify_error_messages(self):
        """
        DESCRIPTION: Verify error messages
        EXPECTED: The error message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: * 'cashoutUpdate' record with 'cashoutValue=0' value is received from MS
        EXPECTED: * 'getBetDetails' request is NOT sent to bpp
        EXPECTED: * 'Cash Out is unavailable because the offer is less than 0.00' message is shown on grey background instead of cashout button
        """
        self.single_bet.scroll_to()
        result = wait_for_result(lambda: self.single_bet.cash_out_error_message == self.expected_message,
                                 name=f'Wait for error message "{self.expected_message}" appear', timeout=15)
        self.assertTrue(result, msg=f'Actual message: "{self.single_bet.cash_out_error_message}" '
                                    f'is not as expected: "{self.expected_message}"')
        self.multiple_bet.scroll_to()
        result = wait_for_result(lambda: self.multiple_bet.cash_out_error_message == self.expected_message,
                                 name=f'Wait for error message "{self.expected_message}" appear', timeout=15)
        self.assertTrue(result, msg=f'Actual message: "{self.multiple_bet.cash_out_error_message}" '
                                    f'is not as expected: "{self.expected_message}"')

    def test_005_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        EXPECTED: * Single bet is shown with the same error message as in step #4
        EXPECTED: * **cashoutValue="0.00"** is received in **getBetDetails?** responce
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Single bet is shown with the same error message as in step #4
        EXPECTED: * **cashoutValue="0.00"** is received in cashoutUpdate via WebSocket
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        if self.device_type == 'desktop':
            self.site.wait_content_state('Homepage', timeout=30)
            self.site.open_my_bets_cashout()
        self.test_002_go_to_single_cash_out_bet_line()
        self.test_004_verify_error_messages()

    def test_006_in_ob_backoffice_return_price_for_events_selection_to_the_previous_value(self):
        """
        DESCRIPTION: In OB Backoffice return price for event's selection to the previous value
        EXPECTED: * 'CASH OUT' button is shown under bet details instead of error message
        """
        self.ob_config.change_price(self.selection_ids[self.team1], self.correct_price)
        self.test_002_go_to_single_cash_out_bet_line()
        self.assertFalse(self.single_bet.has_cash_out_error_message(expected_result=False),
                         msg='Cash Out error message is still displayed')
        self.assertTrue(self.single_bet.buttons_panel.has_full_cashout_button(), msg='Full Cash Out button is not present')
        self.assertFalse(self.multiple_bet.has_cash_out_error_message(expected_result=False),
                         msg='Cash Out error message is still displayed')
        self.assertTrue(self.multiple_bet.buttons_panel.has_full_cashout_button(),
                        msg='Full Cash Out button is not present')

    def test_007_repeat_steps_3_6_for_another_single_bet_during_cash_out_attempt_click_cash_out_and_confirm_cash_out_buttons(self):
        """
        DESCRIPTION: Repeat steps #3-6 for another Single bet during cash out attempt:
        DESCRIPTION: * Click 'CASH OUT' and 'CONFIRM CASH OUT' buttons
        """
        # Covered in above steps

    def test_008_go_to_multiple_cash_out_bet_line_and_repeat_steps_3_8(self):
        """
        DESCRIPTION: Go to **Multiple** Cash Out bet line and repeat steps #3-8
        """
        # Covered in above steps

    def test_009_repeat_steps_1_9_for_partial_cash_out_attempt(self):
        """
        DESCRIPTION: Repeat steps #1-9 for **Partial Cash Out** attempt
        """
        # Covered in above steps
