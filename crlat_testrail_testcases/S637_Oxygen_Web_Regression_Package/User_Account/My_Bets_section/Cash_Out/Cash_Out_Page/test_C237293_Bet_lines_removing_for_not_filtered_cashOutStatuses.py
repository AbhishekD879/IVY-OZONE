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
class Test_C237293_Bet_lines_removing_for_not_filtered_cashOutStatuses(Common):
    """
    TR_ID: C237293
    NAME: Bet lines removing for not filtered cashOutStatuses
    DESCRIPTION: This test case verifies removing bet from 'Cash Out' tab in case getBetDetail request returns cashOutStatus that is not filtered by the proxy
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed Single and Multiple cashout available bets
    PRECONDITIONS: * Web console with Network tab is opened
    PRECONDITIONS: * Backoffice link for event is opened for triggering LiveServe updates: http://backoffice-tst2.coral.co.uk/ti/hierarchy/event/<Event_ID>
    PRECONDITIONS: **cashoutValue filtered by the proxy:**
    PRECONDITIONS: * CASHOUT_SELN_SUSPENDED
    PRECONDITIONS: * CASHOUT_LINE_NO_CASHOUT
    PRECONDITIONS: * DB_ERROR
    PRECONDITIONS: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    PRECONDITIONS: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_cash_out_tab_on_my_betspagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Open Bets'/ 'Cash out' tab on 'My Bets'page/'Bet Slip' widget
        EXPECTED: Placed bets are shown with 'Cashout' button
        """
        pass

    def test_002_in_ob_backoffice_trigger_cashoutstatus_that_is_not_filtered_by_the_proxy_for_event_with_placed_single_bet__ie_cashout_seln_no_cashout_cashoutstatus_via_disabling_cashout_available_option_and_undisplaying_eventmarketselection(self):
        """
        DESCRIPTION: In OB Backoffice trigger cashOutStatus that **is not filtered by the proxy** for event with placed **Single** bet  (i.e. 'CASHOUT_SELN_NO_CASHOUT' cashOutStatus via disabling 'Cashout Available' option and undisplaying event/market/selection)
        EXPECTED: 
        """
        pass

    def test_003_navigate_to_previously_opened_cash_out_page_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened Cash Out page and verify Network tab
        EXPECTED: getBetDetail request is sent
        EXPECTED: **From release XXX.XX:**
        EXPECTED: After switching to Cashout tab new WebSocket connection is created to Cash Out MS
        """
        pass

    def test_004_verify_single_bet_line_with_modified_event_on_cash_out_tab(self):
        """
        DESCRIPTION: Verify **Single** bet line with modified event on 'Cash out' tab
        EXPECTED: - Bet in NOT displayed
        """
        pass

    def test_005_navigate_to_open_bets_tabverify_single_bet_line_with_modified_event_on_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab
        DESCRIPTION: Verify **Single** bet line with modified event on 'Open Bets' tab
        EXPECTED: - Bet is displayed
        EXPECTED: - 'CASH OUT' button is not displayed
        """
        pass

    def test_006_repeat_steps_2_5_for_multiple_bets(self):
        """
        DESCRIPTION: Repeat steps #2-5 for **Multiple** bets
        EXPECTED: 
        """
        pass
