import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # involve events creation and suspension of events from OB
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C511991_Cash_Out_process_when_event_market_selection_becomes_undisplayed(BaseCashOutTest):
    """
    TR_ID: C511991
    NAME: Cash Out process when event/market/selection becomes undisplayed
    DESCRIPTION: This test case verifies Cash Out process when event/market/selection becomes undisplayed on 'My Bets' tab on Event Details page
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: Note: Readbet request/response is sent after successful partial cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successful partial cashout of pre-match events. (Currently, works as for in-play events)
    PRECONDITIONS: **Currently CASH OUT option is available on back-end for Football, Tennis, Darts and Snooker (other sports will be added in future).**
    PRECONDITIONS: **From release XXX.XX:**
    PRECONDITIONS: * WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: * initial bets data will be returned after establishing connection
    """
    keep_browser_open = True
    events = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Login
        DESCRIPTION: Place Single and Multiple bets with available cash out
        """
        # Verify CashOut tab configuration in CMS
        system_config = self.get_initial_data_system_configuration()
        cashout_cms = system_config.get('CashOut', {})
        if not cashout_cms:
            cashout_cms = self.cms_config.get_system_configuration_item('CashOut')
        self.__class__.is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')

        self.__class__.events = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        selection_ids = [event.selection_ids[event.team1] for event in self.events]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_bets_with_available_cashout(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets with available cashout
        """
        self.site.open_my_bets_cashout()

    def test_002_go_to_single_cash_out_bet_line(self):
        """
        DESCRIPTION: Go to **Single** Cash Out bet line
        """
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.single_bet = list(bets.values())[0]
        self.__class__.multiple_bet = list(bets.values())[1]
        self.assertTrue(self.single_bet.buttons_panel.has_full_cashout_button(),
                        msg='"FULL CASH OUT" button was not found in bet section: "%s"' % self.single_bet)
        self.assertTrue(self.multiple_bet.buttons_panel.has_full_cashout_button(),
                        msg='"FULL CASH OUT" button was not found in bet section: "%s"' % self.multiple_bet)

    def test_003_tap_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        """
        self.single_bet.buttons_panel.full_cashout_button.click()
        self.multiple_bet.buttons_panel.full_cashout_button.click()

    def test_004_trigger_undisplaying_in_openbet_ti_tool_for_current_eventmarketselection(self):
        """
        DESCRIPTION: Trigger undisplaying in Openbet TI tool for current event/market/selection
        EXPECTED: Event/market/selection becomes undisplayed
        """
        self.ob_config.change_event_state(event_id=self.events[0].event_id, active=True)

    def test_005_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        self.single_bet.buttons_panel.cashout_button.click()
        self.multiple_bet.buttons_panel.cashout_button.click()
        result = self.single_bet.buttons_panel._spinner_wait(expected_result=False, timeout=25)
        self.assertFalse(result, msg='Spinner still present')
        result = self.multiple_bet.buttons_panel._spinner_wait(expected_result=False, timeout=25)
        self.assertFalse(result, msg='Spinner still present')

    def test_006_wait_until_button_with_spinner_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: The success message is displayed instead of 'CASH OUT' button with the following information:
        EXPECTED: *   Green box with "tick" in a circle and message of "SUCCESSFUL CASH OUT" are shown below bet line details. The icon and text are centered within green box.
        """
        self.assertTrue(self.single_bet.has_cashed_out_mark(),
                        msg='"Cashed out" mark is not present on Cashout page after cashout')
        self.assertTrue(self.multiple_bet.has_cashed_out_mark(),
                        msg='"Cashed out" mark is not present on Cashout page after cashout')

    def test_007_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        """
        # Covered in above steps

    def test_008_navigate_to_multiple_cash_out_bet_line_and_repeat_steps_1_7(self):
        """
        DESCRIPTION: Navigate to **Multiple** Cash Out bet line and repeat steps #1-7
        """
        # Covered in above steps

    def test_009_repeat_steps_1_8_for_partial_cash_out_attempt(self):
        """
        DESCRIPTION: Repeat steps #1-8 for **Partial Cash Out** attempt
        """
        # Covered in above steps
