import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C237389_Bet_lines_update_after_not_filtered_cashOutStatuses(Common):
    """
    TR_ID: C237389
    NAME: Bet lines update after not filtered cashOutStatuses
    DESCRIPTION: This test case verifies updating bet line on 'My Bets' tab in case getBetDetail request returns cashOutStatus that is not filtered by the proxy
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed Single and Multiple cashout available bets
    PRECONDITIONS: * Web console with Network tab is opened
    PRECONDITIONS: * Backoffice link for event is opened for triggering LiveServe notifications: http://backoffice-tst2.coral.co.uk/ti/hierarchy/event/<Event_ID>
    PRECONDITIONS: **Statuses filtered by the proxy:**
    PRECONDITIONS: * CASHOUT_SELN_SUSPENDED/CASHOUT_LEGSORT_NOT_ALLOWED
    PRECONDITIONS: * CASHOUT_SELN_NO_CASHOUT
    PRECONDITIONS: * DB_ERROR
    PRECONDITIONS: * " " - this one is when Cash Out is available and "cashoutValue: <Number>" is also sent
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * getBetDetail request sometimes returns obsolete response, in this case it should be triggered one more time
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_single_bet_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Single** bet with available cash out
        EXPECTED: **Single** bet  is shown with 'FULL CASH OUT' and 'PARTIAL CASH OUT' buttons
        """
        pass

    def test_002_in_ob_backoffice_trigger_cashoutstatus_that_is_not_filtered_by_the_proxy_for_event_with_placed_single_bet__ie_cashout_seln_no_cashout_cashoutstatus_via_disabling_cashout_available_option_and_undisplaying_eventmarketselection(self):
        """
        DESCRIPTION: In OB Backoffice trigger cashOutStatus that **is not filtered by the proxy** for event with placed **Single** bet  (i.e. 'CASHOUT_SELN_NO_CASHOUT' cashOutStatus via disabling 'Cashout Available' option and undisplaying event/market/selection)
        EXPECTED: 
        """
        pass

    def test_003_refresh_page_my_bets_tab_on_event_details_page_and_verify_network_tab(self):
        """
        DESCRIPTION: Refresh page: 'My bets' tab on Event Details page and verify Network tab
        EXPECTED: * push notification with changed values is received
        EXPECTED: * getBetDetail request is sent
        EXPECTED: * status not filtered by proxy (i.e. SELN_NO_CASHOUT) is shown in response
        """
        pass

    def test_004_verify_single_bet_line_with_modified_event(self):
        """
        DESCRIPTION: Verify **Single** bet line with modified event
        EXPECTED: * Bet is displayed
        EXPECTED: * 'FULL CASH OUT' and 'PARTIAL CASH OUT' buttons are not shown
        """
        pass

    def test_005_reopen_page_refresh_page(self):
        """
        DESCRIPTION: Reopen page/ Refresh page
        EXPECTED: * Bet is displayed as a normal non-Cash Out bet
        EXPECTED: * 'FULL CASH OUT' and 'PARTIAL CASH OUT' buttons are not shown
        """
        pass

    def test_006_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_single_bet__with_cashoutstatus_that_is_filtered_by_the_proxy_eg_cashout_seln_suspendedcashout_legsort_not_allowed___event_is_suspended(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Single** bet  with cashOutStatus that **is filtered by the proxy** (e.g. 'CASHOUT_SELN_SUSPENDED/CASHOUT_LEGSORT_NOT_ALLOWED' - event is suspended)
        EXPECTED: **Single** bet line is shown with error message instead of 'CASH OUT' button
        """
        pass

    def test_007_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps #2-5
        EXPECTED: 
        """
        pass

    def test_008_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_multiple_bet_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Multiple** bet with available cash out
        EXPECTED: **Multiple** bet line is shown with enabled 'CASH OUT' and 'Partial CashOut' buttons
        """
        pass

    def test_009_repeat_steps_2_5_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #2-5 for **Multiple** bet
        EXPECTED: 
        """
        pass

    def test_010_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_multiple_bet__with_cashoutstatus_that_is_filtered_by_the_proxy_eg_cashout_seln_suspendedcashout_legsort_not_allowed___event_is_suspended(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Multiple** bet  with cashOutStatus that **is filtered by the proxy** (e.g. 'CASHOUT_SELN_SUSPENDED/CASHOUT_LEGSORT_NOT_ALLOWED' - event is suspended)
        EXPECTED: **Multiple** bet line is shown with error message instead of 'CASH OUT' button
        """
        pass

    def test_011_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps #2-5
        EXPECTED: 
        """
        pass
