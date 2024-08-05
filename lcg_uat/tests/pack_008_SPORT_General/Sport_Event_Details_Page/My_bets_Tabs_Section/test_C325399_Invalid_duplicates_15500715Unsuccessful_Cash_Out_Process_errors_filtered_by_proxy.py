import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.prod # involve events creation and suspension of events from OB
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.cash_out
@vtest
class Test_C325399_Invalid_duplicates_15500715Unsuccessful_Cash_Out_Process_errors_filtered_by_proxy(BaseCashOutTest):
    """
    TR_ID: C325399
    NAME: [Invalid-duplicates 15500715]Unsuccessful Cash Out Process (errors filtered by proxy)
    DESCRIPTION: This test case verifies unsuccessful Full and Partial Cash Out Process because of errors filtered by proxy on 'My Bets' tab on Event Details page
    DESCRIPTION: Need to update test case according to https://jira.egalacoral.com/browse/BMA-39080
    DESCRIPTION: Step 5 not valid - Errors disappear and button 'Cashout Suspended' displayed
    DESCRIPTION: Test case is not valid as the flow is covered in https://ladbrokescoral.testrail.com//index.php?/cases/view/15500715
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: **cashoutStatuses filtered by the proxy:**
    PRECONDITIONS: * CASHOUT_SELN_SUSPENDED/CASHOUT_LEGSORT_NOT_ALLOWED
    PRECONDITIONS: * CASHOUT_SELN_NO_CASHOUT
    PRECONDITIONS: * DB_ERROR
    PRECONDITIONS: Note: Readbet request/response is sent after successful partial/full cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successful partial/full cashout of pre-match events. (Currently, works as for in-play events)
    PRECONDITIONS: [How to use Fiddler][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+mock+proxy+responses+using+Fiddler
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
        bet_name, single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=self.created_event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, number_of_bets=5)
        event_names = [self.created_event_name, self.created_event_name2]
        bet_name, multiple_bet = self.site.cashout.tab_content.accordions_list.get_bet(event_names=event_names)
        self.assertTrue(single_bet.buttons_panel.has_full_cashout_button(),
                        msg='"FULL CASH OUT" button was not found in bet section: "%s"' % single_bet)
        self.assertTrue(multiple_bet.buttons_panel.has_full_cashout_button(),
                        msg='"FULL CASH OUT" button was not found in bet section: "%s"' % multiple_bet)
        self.assertTrue(single_bet.buttons_panel.has_partial_cashout_button(),
                        msg='"PARTIAL CASH OUT" button was not found in bet section: "%s"' % single_bet)
        self.assertTrue(multiple_bet.buttons_panel.has_partial_cashout_button(),
                        msg='"PARTIAL CASH OUT" button was not found in bet section: "%s"' % multiple_bet)

    def test_003_trigger_suberrorcode_cashout_seln_suspended_or_cashout_legsort_not_allowed_for_cashoutbet_response_during_cash_out_attempt_suspend_event_or_market_or_selection_for_event_with_placed_bet_in_backoffice_immediately_click_cash_out_and_confrim_cash_out_buttons(self):
        """
        DESCRIPTION: Trigger subErrorCode 'CASHOUT_SELN_SUSPENDED' OR 'CASHOUT_LEGSORT_NOT_ALLOWED' for **cashoutBet** response during cash out attempt:
        DESCRIPTION: * Suspend event or market or selection for event with placed bet in backoffice
        DESCRIPTION: * Immediately click 'CASH OUT' and 'CONFRIM CASH OUT' buttons
        EXPECTED: * Error messages are displayed
        EXPECTED: * User balance is not updated
        """
        sleep(2)
        self.ob_config.change_event_cashout_status(event_id=self.events[0].event_id, cashout_available=False)
        sleep(2)
        self.ob_config.change_event_state(event_id=self.events[0].event_id)

    def test_004_verify_error_messages(self):
        """
        DESCRIPTION: Verify error messages
        EXPECTED: The error message is displayed instead of 'CASH OUT' button with the following information:
        EXPECTED: * Message box with an "X" in a circle and message of 'CASH OUT UNSUCCESSFUL'  is shown below bet line details. Icon and text are centered.
        EXPECTED: * Underneath previous box second message is displayed with centered text **'Your Cash Out attempt was unsuccessful, your selection is suspended.'**
        """
        bet_name, single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=self.created_event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, number_of_bets=5)
        event_names = [self.created_event_name, self.created_event_name2]
        bet_name, multiple_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=event_names)
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
        EXPECTED: * Errors don't change to other error messages if any are received after cash out attempt
        EXPECTED: * Errors disappear ONLY when bet becomes cash out available again
        EXPECTED: * After page refresh errors changes to the one described in TC 238033
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        sleep(2)
        self.test_004_verify_error_messages()

    def test_006_navigate_to_another_single_bet_and_trigger_suberrorcode_cashout_seln_suspended_or_cashout_legsort_not_allowed_for_readbet_response_during_cash_out_attempt_click_cash_out_and_confrim_cash_out_buttons_immediately_suspend_event_or_market_or_selection_for_event_with_placed_bet_in_backoffice(self):
        """
        DESCRIPTION: Navigate to another Single bet and trigger subErrorCode 'CASHOUT_SELN_SUSPENDED' OR 'CASHOUT_LEGSORT_NOT_ALLOWED' for **readBet** response during cash out attempt:
        DESCRIPTION: * Click 'CASH OUT' and 'CONFRIM CASH OUT' buttons
        DESCRIPTION: * Immediately suspend event or market or selection for event with placed bet in backoffice
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
        EXPECTED: Results are the same except another error message in step #4:
        EXPECTED: * Underneath previous box second message is displayed with centered text **'Your Cash Out attempt was unsuccessful, at least one of your selections is suspended.'**
        """
        # Covered in above steps

    def test_010_repeat_steps_2_9_for_cashoutvalue_with_cashoutstatus_filtered_by_proxy_db_error_using_fiddler_tool(self):
        """
        DESCRIPTION: Repeat steps #2-9 for 'cashoutValue' with cashOutStatus filtered by proxy DB_ERROR using Fiddler tool
        EXPECTED: Results are the same except in step #4
        EXPECTED: * Underneath previous box second message is not shown
        """
        # Covered in above steps

    def test_011_repeat_steps_2_9_for__cashoutvalue_with_cashoutstatus_filtered_by_proxy_cashout_seln_no_cashout_which_can_be_triggered_by_disabling_cashout_available_option(self):
        """
        DESCRIPTION: Repeat steps #2-9 for  'cashoutValue' with cashOutStatus filtered by proxy CASHOUT_SELN_NO_CASHOUT which can be triggered by disabling 'Cashout Available' option
        EXPECTED: Results are the same except in step #4
        EXPECTED: * Underneath previous box second message is not shown
        """
        # Covered in above steps

    def test_012_verify_errors_displaying_logic(self):
        """
        DESCRIPTION: Verify errors displaying logic
        EXPECTED: * Errors don't disappear after scrolling up and down or collapsing-expanding bet accordion
        EXPECTED: * After 5 seconds **bet with error is removed** from the Cash Out section
        EXPECTED: * After page refresh bet is not displayed on the Cash Out section
        """
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
