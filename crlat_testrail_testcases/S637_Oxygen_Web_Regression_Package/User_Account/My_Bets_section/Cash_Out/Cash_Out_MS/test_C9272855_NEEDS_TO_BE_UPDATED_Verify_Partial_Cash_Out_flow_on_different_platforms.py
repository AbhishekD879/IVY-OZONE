import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.cash_out
@vtest
class Test_C9272855_NEEDS_TO_BE_UPDATED_Verify_Partial_Cash_Out_flow_on_different_platforms(Common):
    """
    TR_ID: C9272855
    NAME: [NEEDS TO BE UPDATED] Verify Partial Cash Out flow on different platforms
    DESCRIPTION: This test case verifies partial Cash Out flow when Cash out MS is turned on different devices
    DESCRIPTION: To be updated: Correct version should be set instead of XXX.XX
    DESCRIPTION: **From release XXX.XX (according to BMA-50940/BMA-50937):**
    DESCRIPTION: - WS connection to Cashout MS is created when user lands on myBets page
    DESCRIPTION: - No requests to BPP getBetDetails and getBetDetail should be performed on cashout page
    PRECONDITIONS: In CMS
    PRECONDITIONS: * Load CMS and log in
    PRECONDITIONS: * Go to System Configuration section
    PRECONDITIONS: * Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: In Oxygen app
    PRECONDITIONS: * Load app and log in with the same user on at list 2 devices under the same network
    PRECONDITIONS: * Place a few bets (Single and Multiple) with CashOut available option
    PRECONDITIONS: * Open Dev Tools -> Network tab -> XHR filter
    PRECONDITIONS: Endpoints to CashOut MS
    PRECONDITIONS: * https://cashout-dev1.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev1
    PRECONDITIONS: * https://cashout-dev0.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev0
    PRECONDITIONS: where token - bpp token
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_pagetab_for_tablet_or_desktop_on_the_first_device(self):
        """
        DESCRIPTION: Navigate to Cash Out page/tab for Tablet or Desktop on the first device
        EXPECTED: * EventStream connection is created to Cash Out MS
        EXPECTED: * Content of Cash Out page/tab is loaded
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * WS connection to Cashout MS is created
        EXPECTED: * Content of Cash Out page/tab is loaded
        """
        pass

    def test_002_navigate_to_cash_out_pagetab_for_tablet_or_desktop_on_the_second_device(self):
        """
        DESCRIPTION: Navigate to Cash Out page/tab for Tablet or Desktop on the second device
        EXPECTED: * EventStream connection is created to Cash Out MS
        EXPECTED: * Content of Cash Out page/tab is loaded
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * WS connection to Cashout MS is created
        EXPECTED: * Content of Cash Out page/tab is loaded
        """
        pass

    def test_003_go_to_single_cash_out_bet_on_the_first_device(self):
        """
        DESCRIPTION: Go to **Single** Cash Out bet on the first device
        EXPECTED: 
        """
        pass

    def test_004_click_on_partial_cashout_button(self):
        """
        DESCRIPTION: Click on 'Partial CashOut' button
        EXPECTED: 'Partial CashOut' slider is shown
        """
        pass

    def test_005_set_pointer_on_the_bar_to_any_value_not_to_maximum_and_tap_cashout_button(self):
        """
        DESCRIPTION: Set pointer on the bar to any value (not to maximum) and tap 'CashOut' button
        EXPECTED: 'CONFIRM CASH OUT <currency> partial cashOut value' button is shown
        EXPECTED: where 'currency' is the same as during registration
        EXPECTED: cashOut value - value that user is going to cash out
        """
        pass

    def test_006_tap_confirm_cash_out_currency_partial_cashout_value_and_trigger_successful_partial_cash(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT <currency> partial cashOut value' and trigger successful Partial Cash
        EXPECTED: * Partial Cash out is successful
        EXPECTED: * Update with type **event:betUpdate** is received from Cash Out MS
        EXPECTED: * Previous EventStream connection is closed
        EXPECTED: * New connection to Cash Out MS is created
        EXPECTED: * 'Stake' and 'Est. Returns' values are decreased for bet
        EXPECTED: * New Cash Out value is displayed on 'Cash Out' button
        EXPECTED: Actual from 103 release for both brands:
        EXPECTED: * Partial Cash out is successful.
        EXPECTED: * Current EventStream connection is NOT closed.
        EXPECTED: * New connection to Cash Out MS is NOT created.
        EXPECTED: * Update with type **event:betUpdate** is received from Cash Out MS in the current /bet-details connection.
        EXPECTED: * Frontend should not make /getBetDetail call to BPP after successful partial cashout.
        EXPECTED: * 'Stake' and 'Est. Returns' values are decreased for bet
        EXPECTED: * New Cash Out value is displayed on 'Cash Out' button
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Partial Cash Out is successful
        EXPECTED: * No requests to BPP getBetDetails and getBetDetail should be performed on cashout page
        EXPECTED: * Only one current connection to cashout MS should be active on cashout page
        EXPECTED: * Bet info should be updated with data from extended responses from cashoutBet or readBet requests
        EXPECTED: * 'Stake' and 'Est. Returns' values are decreased for bet
        EXPECTED: * New Cash Out value is displayed on 'Cash Out' button
        """
        pass

    def test_007_go_to_the_second_device_and_verify_single_cash_out_bet(self):
        """
        DESCRIPTION: Go to the second device and verify **Single** Cash Out bet
        EXPECTED: **Until release XXX.XX:**
        EXPECTED: * Update with type **event:betUpdate** is received from Cash Out MS
        EXPECTED: * 'Stake' and 'Est. Returns' values are decreased for bet
        EXPECTED: * New Cash Out value is displayed on 'Cash Out' button
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * New Cash Out value is not automatically updated
        EXPECTED: * User balance is updated after cash out on first device
        """
        pass

    def test_008_try_to_make_partial_cash_out_on_second_device(self):
        """
        DESCRIPTION: Try to make Partial Cash Out on second device
        EXPECTED: * Valid error message is displayed
        EXPECTED: * Bet receives updated values
        """
        pass

    def test_009_go_to_multiple_cash_out_bet_on_the_first_device(self):
        """
        DESCRIPTION: Go to **Multiple** Cash Out bet on the first device
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_4_8_for_multiple_cash_out_bet(self):
        """
        DESCRIPTION: Repeat steps #4-8 for Multiple Cash Out bet
        EXPECTED: 
        """
        pass
