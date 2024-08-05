import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.prod # involve events creation and suspension of events from OB
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C325400_Unsuccessful_Cash_Out_Process_errors_NOT_filtered_by_proxy(BaseCashOutTest):
    """
    TR_ID: C325400
    NAME: Unsuccessful Cash Out Process (errors NOT filtered by proxy)
    DESCRIPTION: This test case verifies unsuccessful Full and Partial Cash Out Process because of errors NOT filtered by proxy on 'My Bets' tab on Event Details page
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: Note: Readbet request/response is sent after successful partial/full cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successful partial/full cashout of pre-match events. (Currently, works as for in-play events)
    PRECONDITIONS: [How to use Fiddler][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+mock+proxy+responses+using+Fiddler
    PRECONDITIONS: [How to trigger specific 'subErrorCodes'][2]
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/pages/viewpage.action?pageId=58391155
    PRECONDITIONS: **From release XXX.XX:**
    PRECONDITIONS: - Open Dev Tools -> Network tab -> WS filter (cashout request)
    PRECONDITIONS: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: - initial bets data will be returned after establishing connection
    """
    keep_browser_open = True
    events = None
    created_event_name, created_event_name2 = None, None

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
        self.__class__.created_event_name = '%s %s' % (self.events[0].event_name, self.events[0].local_start_time)
        self.__class__.created_event_name2 = '%s %s' % (self.events[1].event_name, self.events[1].local_start_time)
        self.site.login()
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_bets_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets with available cash out
        """
        self.site.open_my_bets_cashout()

    def test_002_navigate_to_the_single_bet(self):
        """
        DESCRIPTION: Navigate to the **Single** bet
        """
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        single_bet = list(bets.values())[0]
        multiple_bet = list(bets.values())[1]
        self.assertTrue(single_bet.buttons_panel.has_full_cashout_button(),
                        msg='"FULL CASH OUT" button was not found in bet section: "%s"' % single_bet)
        self.assertTrue(multiple_bet.buttons_panel.has_full_cashout_button(),
                        msg='"FULL CASH OUT" button was not found in bet section: "%s"' % multiple_bet)

    def test_003_trigger_suberrorcode_cashout_unavailable_cust_no_cashout_or_cashout_cust_restrict_flag_for_cashoutbet_response_during_cash_out_attempt_suspend_event_or_market_or_selection_for_event_with_placed_bet_in_backoffice_immediately_click_cash_out_and_confrim_cash_out_buttons_using_fiddler_tool_mock_response_in_cashoutbet_response(self):
        """
        DESCRIPTION: Trigger subErrorCode 'CASHOUT_UNAVAILABLE_CUST_NO_CASHOUT' OR 'CASHOUT_CUST_RESTRICT_FLAG' for **cashoutBet** response during cash out attempt:
        DESCRIPTION: * Suspend event or market or selection for event with placed bet in backoffice
        DESCRIPTION: * Immediately click 'CASH OUT' and 'CONFRIM CASH OUT' buttons
        DESCRIPTION: * Using **Fiddler tool mock** response in cashoutBet response
        EXPECTED: * Error messages are displayed
        EXPECTED: * User balance is not updated
        """
        sleep(2)
        self.ob_config.change_event_cashout_status(event_id=self.events[0].event_id, cashout_available=False)
        self.ob_config.change_event_cashout_status(event_id=self.events[1].event_id, cashout_available=False)
        sleep(2)
        self.ob_config.change_event_state(event_id=self.events[0].event_id)
        self.ob_config.change_event_state(event_id=self.events[1].event_id)

    def test_004_verify_error_messages(self):
        """
        DESCRIPTION: Verify error messages
        EXPECTED: The error message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: * Message box with an "X" in a circle and message of 'CASH OUT UNSUCCESSFUL'  is shown below bet line details. Icon and text are centered.
        EXPECTED: * Underneath previous box second message is displayed with centered text **'Your Cash Out attempt was unsuccessful, your account is not eligible to receive Cash Out offers.'**
        """
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        single_bet = list(bets.values())[0]
        multiple_bet = list(bets.values())[1]
        cashout_suspended = single_bet.buttons_panel.cashout_button.label
        self.assertEqual(cashout_suspended, vec.bet_history.CASHOUT_BET.cash_out_bet_suspended,
                         msg=f'Actual message: "{cashout_suspended}", is not the same '
                             f'as expected: "{vec.bet_history.CASHOUT_BET.cash_out_bet_suspended}"')
        not_available_message = multiple_bet.buttons_panel.cashout_button.label
        self.assertEqual(not_available_message, vec.bet_history.CASHOUT_BET.cash_out_bet_suspended,
                         msg=f'Actual message: "{not_available_message}", is not the same '
                             f'as expected: "{vec.bet_history.CASHOUT_BET.cash_out_bet_suspended}"')
        self.assertFalse(
            single_bet.buttons_panel.has_full_cashout_button(expected_result=False, timeout=10),
            msg=f'"FULL CASH OUT" button was found in bet section: "{single_bet}"')
        self.assertFalse(multiple_bet.buttons_panel.has_full_cashout_button(expected_result=False),
                         msg=f'"FULL CASH OUT" button was found in bet section: "{multiple_bet}"')
        self.assertFalse(single_bet.buttons_panel.has_partial_cashout_button(expected_result=False),
                         msg='"PARTIAL CASH OUT" button was not found in bet section: "%s"' % single_bet)
        self.assertFalse(multiple_bet.buttons_panel.has_partial_cashout_button(expected_result=False),
                         msg='"PARTIAL CASH OUT" button was not found in bet section: "%s"' % multiple_bet)

    def test_005_verify_errors_displaying_logic(self):
        """
        DESCRIPTION: Verify errors displaying logic
        EXPECTED: * Errors don't disappear after scrolling up and down or collapsing-expanding bet accordion
        EXPECTED: * After 5 seconds error disappears and bet is displayed as a normal non-Cash Out bet (without 'CASH OUT' button and slider)
        EXPECTED: * After page refresh bet is displayed as a normal non-Cash Out bet without error
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        sleep(2)
        self.test_004_verify_error_messages()
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        if self.device_type == 'desktop':
            self.site.wait_content_state('Homepage', timeout=30)
            self.site.open_my_bets_cashout()
        single_bet_name, single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=self.created_event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
            raise_exceptions=False,
            number_of_bets=5)
        event_names = [self.created_event_name, self.created_event_name2]
        multiple_bet_name, multiple_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=event_names, raise_exceptions=False)
        if self.is_cashout_tab_enabled:
            self.assertFalse(single_bet,
                             msg=f'Event: "{self.created_event_name}" single Bet is shown on Cashout page')
            self.assertFalse(multiple_bet, msg='Multiple Bet is shown on Cashout page')
        else:
            self.assertTrue(single_bet,
                            msg=f'Event: "{self.created_event_name}" single Bet is not shown on Cashout page')
            self.assertFalse(single_bet.buttons_panel.has_full_cashout_button(expected_result=False),
                             msg=f'Full Cash Out button is enabled for event "{self.created_event_name}"')
            self.assertTrue(multiple_bet, msg='Multiple Bet is not shown on Cashout page')
            self.assertFalse(multiple_bet.buttons_panel.has_full_cashout_button(expected_result=False),
                             msg='Full Cash Out button is enabled')

    def test_006_navigate_to_another_single_bet_and_trigger_suberrorcode_cashout_unavailable_cust_no_cashout_or_cashout_cust_restrict_flag_for_readbet_response_during_cash_out_attempt_click_cash_out_and_confrim_cash_out_buttons_immediately_suspend_event_or_market_or_selection_for_event_with_placed_bet_in_backoffice_using_fiddler_tool_mock_response_in_readbet_response(self):
        """
        DESCRIPTION: Navigate to another Single bet and trigger subErrorCode 'CASHOUT_UNAVAILABLE_CUST_NO_CASHOUT' OR 'CASHOUT_CUST_RESTRICT_FLAG' for **readBet** response during cash out attempt:
        DESCRIPTION: * Click 'CASH OUT' and 'CONFRIM CASH OUT' buttons
        DESCRIPTION: * Immediately suspend event or market or selection for event with placed bet in backoffice
        DESCRIPTION: * Using **Fiddler tool mock** response in readBet response
        EXPECTED:
        """
        # Covered in above steps

    def test_007_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps #4-5
        EXPECTED: Results are the same
        """
        # Covered in above steps

    def test_008_repeats_steps_3_7_for_partial_cash_out_attempt(self):
        """
        DESCRIPTION: Repeats steps #3-7 for **Partial** Cash Out attempt
        EXPECTED: Results are the same
        """
        # Covered in above steps

    def test_009_repeat_steps_3_8_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #3-8 for **Multiple** bet
        EXPECTED: Results are the same
        """
        # Covered in above steps

    def test_010_repeat_steps_2_9_for_suberrorcode_cashout_bet_cashed_out(self):
        """
        DESCRIPTION: Repeat steps #2-9 for subErrorCode 'CASHOUT_BET_CASHED_OUT'
        EXPECTED: Results are the same except another error message in step #4:
        EXPECTED: * Underneath previous box second message is displayed with centered text **'Your Cash Out attempt was unsuccessful, as your bet has already been Cashed Out.'**
        """
        # Covered in above steps

    def test_011_repeat_steps_2_9_for_suberrorcode_cashout_bet_settled(self):
        """
        DESCRIPTION: Repeat steps #2-9 for subErrorCode 'CASHOUT_BET_SETTLED'
        EXPECTED: Results are the same except another error message in step #4:
        EXPECTED: * Underneath previous box second message is displayed with centered text **'Your Cash Out attempt was unsuccessful, as your bet has already been settled.'**
        """
        # Covered in above steps

    def test_012_repeat_steps_2_9_for_any_other_suberrorcode_not_filtered_by_proxy_for_example_cashout_unavailable__sys_no_cashout_using_fiddler_tool(self):
        """
        DESCRIPTION: Repeat steps #2-9 for any other subErrorCode not filtered by proxy (for example 'CASHOUT_UNAVAILABLE_ SYS_NO_CASHOUT' (using Fiddler tool))
        EXPECTED: Results are the same except in step #4:
        EXPECTED: * Underneath previous box second message is not shown
        """
        # Covered in above steps

    def test_013_repeat_steps_2_9_for_absence_of_suberrorcode__using_fiddler_tool(self):
        """
        DESCRIPTION: Repeat steps #2-9 for absence of subErrorCode  (using Fiddler tool)
        EXPECTED: Results are the same except in step #4:
        EXPECTED: * Underneath previous box second message is not shown
        """
        # Covered in above steps
