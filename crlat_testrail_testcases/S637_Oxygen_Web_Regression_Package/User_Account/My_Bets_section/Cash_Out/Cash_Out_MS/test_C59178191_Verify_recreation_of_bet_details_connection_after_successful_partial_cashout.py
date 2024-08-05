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
class Test_C59178191_Verify_recreation_of_bet_details_connection_after_successful_partial_cashout(Common):
    """
    TR_ID: C59178191
    NAME: Verify recreation of  bet-details connection after successful partial cashout
    DESCRIPTION: This test case verifies that request to /getBetDetail from BPP is not sent after successful partial cashout and connection to /bet-details stream wasn't recreated for both brands
    PRECONDITIONS: Actual from Release 103 for both brands according to https://jira.egalacoral.com/browse/BMA-53660
    PRECONDITIONS: New Cashout is enabled in CMS: (System config -> Cashout-> 'isV4Enabled')
    PRECONDITIONS: OB TIs:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+OpenBet+System
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User is on Cashout/Open Bets tabs
    PRECONDITIONS: * User has placed single/multiple bets with cashout available and partial cashout available
    PRECONDITIONS: * 'EventStream connection' is created to Cash Out MS in 'bet-details' request
    PRECONDITIONS: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    PRECONDITIONS: * WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: * initial bets data will be returned after establishing connection
    """
    keep_browser_open = True

    def test_001_click_on_partial_cashout_button_on_any_bet_singlemultiple_and_confirm_it(self):
        """
        DESCRIPTION: Click on 'Partial Cashout' button on any bet (single/multiple) and confirm it
        EXPECTED: * Partial Cash Out is successful
        EXPECTED: * No new connection is created to Cash Out MS (for partial cashout)
        EXPECTED: * Current connection stays in pending status: not closing (for partial cashout)
        EXPECTED: * BetUpdate about new stake is received in same active connection
        EXPECTED: * No request to /getBetDetail from BPP
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Partial Cash Out is successful
        EXPECTED: * no requests to BPP getBetDetails and getBetDetail should be performed on cashout page
        EXPECTED: * only one current connection to cashout MS should be active on cashout page
        EXPECTED: * bet info should be updated with data from extended responses from cashoutBet or readBet requests
        """
        pass

    def test_002_in_ti_trigger_bet_update_price_changesuspend_again_this_bet_and_check_the_connection(self):
        """
        DESCRIPTION: In TI trigger bet update (price change/suspend) again this bet and check the connection
        EXPECTED: * No new EventStream connection is created
        EXPECTED: * Updates like cashout/bet updates are received in same active connection
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Cashout MS will send cashoutUpdate message with updated cashout value after price update
        """
        pass

    def test_003_perform_unsuccessful_partial_cashouteg_turn_off_internet_connection_and_tap_partial_cashout_button(self):
        """
        DESCRIPTION: Perform unsuccessful Partial Cashout
        DESCRIPTION: e.g turn off internet connection and tap 'Partial Cashout' button
        EXPECTED: * Partial cash out is unsuccessful
        EXPECTED: * Previous EventStream connection is finished (see Timing tab of request)
        EXPECTED: * New connection is created to Cash Out MS
        EXPECTED: * Connection stays in pending status (not closing)
        EXPECTED: * Update with type event:initial is received from Cash Out MS
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Partial cash out is unsuccessful
        EXPECTED: * after unsuccessful cashout old WebSocket connection to Cashout MS should be closed and new one should be established to update bets states
        EXPECTED: * no requests to BPP getBetDetails and getBetDetail should be performed on cashout page
        """
        pass

    def test_004_repeat_steps_above_for_the_open_betscashout_tabs_in_widgetsdesktop(self):
        """
        DESCRIPTION: Repeat steps above for the Open bets/Cashout tabs in widgets/desktop
        EXPECTED: Results are the same
        EXPECTED: NOTE: after switching to Open Bets tab or Cashout tab:
        EXPECTED: - New connection is created to Cash Out MS
        EXPECTED: - Previous EventStream connection is finished (see Timing tab of request)
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Results are the same
        EXPECTED: * WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
        """
        pass
