import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2069257_Verify_Cash_Out_when_value_DECREASES_INCREASES(Common):
    """
    TR_ID: C2069257
    NAME: Verify Cash Out when value DECREASES/INCREASES
    DESCRIPTION: This test case verifies Cash Out functionality when cash out value increases/decreases during cash out process.
    PRECONDITIONS: 1.  Valid Cash Out Coupon Code should be generated (support is needed from RCOMB team)
    PRECONDITIONS: 2.  To find all details related to the coupon open browser console (F12) -> Network -> request 'coupon?id=<coupon code>' -> Preview
    PRECONDITIONS: 3.  To find all details related to the cashed out coupon open browser console (F12) -> Network -> request 'readbet?delayId=<delayId>' -> Preview -> bet
    PRECONDITIONS: 4.  Go to ATM Amelco to trigger price changing
    PRECONDITIONS: *Cash Out is available when at least one bet's event is started*
    PRECONDITIONS: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    """
    keep_browser_open = True

    def test_001__load_sportbook_app_log_in_chose_connect_from_header_ribbon_select_shop_bet_tracker(self):
        """
        DESCRIPTION: * Load Sportbook App
        DESCRIPTION: * Log in
        DESCRIPTION: * Chose 'Connect' from header ribbon
        DESCRIPTION: * Select 'Shop Bet Tracker'
        EXPECTED: RCOMB microsite is opened representing Home Entry Screen
        """
        pass

    def test_002_submit_valid_cash_out_code_which_containssingleselection_available_for_cash_out(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains **Single **selection available for cash out
        EXPECTED: *   Cash Out Code is submitted successfully
        EXPECTED: *   Cash Out Coupon is shown to the user expanded by default
        """
        pass

    def test_003_tap_cash_out_xxxx_button(self):
        """
        DESCRIPTION: Tap 'CASH OUT XX.XX' button
        EXPECTED: *   The button text changes to "CONFIRM"
        EXPECTED: *   "CONFIRM" button is enabled
        EXPECTED: *   The same cash out value is shown on button in format XX.XX
        """
        pass

    def test_004_trigger_situation_whencash_out_valuedecreasesduring_cash_out_process_after_tapping_confirm_buttonnote_priceodds_should_be_increased(self):
        """
        DESCRIPTION: Trigger situation when cash out value **decreases **during cash out process (after tapping 'CONFIRM' button)
        DESCRIPTION: Note: Price/Odds should be increased
        EXPECTED: 
        """
        pass

    def test_005_tap_confirm_xxxx_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM XX.XX' button
        EXPECTED: *   The button text changes to loading spinner
        EXPECTED: *   Button is disabled
        """
        pass

    def test_006_wait_untilloading_spinner_disappears(self):
        """
        DESCRIPTION: Wait until loading spinner disappears
        EXPECTED: *   The button text changes to "CONFIRM"
        EXPECTED: *   "CONFIRM" button is enabled
        EXPECTED: *   **New**** cash out value** is shown on "CONFIRM" button in format XX.XX
        EXPECTED: *   Tooltip with an error message **"Your Cash Out value for this bet has changed"** is displayed
        EXPECTED: *   Bet remains not cashed out
        """
        pass

    def test_007_verify_tooltipwith_an_error_message(self):
        """
        DESCRIPTION: Verify tooltip with an error message
        EXPECTED: Tooltip with an error message **"Your Cash Out value for this bet has changed"** disappears in 5 seconds or after tapping "CONFIRM" button
        """
        pass

    def test_008_tap_cash_out_xxxx_button(self):
        """
        DESCRIPTION: Tap 'CASH OUT XX.XX' button
        EXPECTED: *   The button text changes to "CONFIRM"
        EXPECTED: *   "CONFIRM" button is enabled
        EXPECTED: *   The same cash out value is shown on button in format XX.XX
        """
        pass

    def test_009_trigger_situation_whencash_out_valueincreasedduring_cash_out_process_after_tapping_confirm_buttonnote_priceodds_should_be_decreased(self):
        """
        DESCRIPTION: Trigger situation when cash out value **increased **during cash out process (after tapping 'CONFIRM' button)
        DESCRIPTION: Note: Price/Odds should be decreased
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_5_7(self):
        """
        DESCRIPTION: Repeat steps #5-7
        EXPECTED: 
        """
        pass

    def test_011_go_to_my_bets__in_shop_bets__sub_tub__verify_cash_out_functionality_there_repeat_steps_3_10(self):
        """
        DESCRIPTION: Go to 'My Bets' ->'In-Shop Bets'  sub-tub ->
        DESCRIPTION: verify cash out functionality there (repeat steps #3-10)
        EXPECTED: 
        """
        pass
