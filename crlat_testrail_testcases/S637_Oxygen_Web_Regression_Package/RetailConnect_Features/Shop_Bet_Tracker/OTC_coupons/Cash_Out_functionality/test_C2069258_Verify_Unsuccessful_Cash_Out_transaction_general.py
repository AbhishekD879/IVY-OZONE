import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2069258_Verify_Unsuccessful_Cash_Out_transaction_general(Common):
    """
    TR_ID: C2069258
    NAME: Verify Unsuccessful Cash Out transaction (general)
    DESCRIPTION: This test case verifies Unsuccessful Cash Out transaction.
    DESCRIPTION: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    PRECONDITIONS: *   Valid Cash Out Coupon Code should be generated (support is needed from RCOMB team)
    PRECONDITIONS: *   RCOMB team support is needed to trigger errors
    PRECONDITIONS: *   To find all details related to the coupon open browser console (F12) -> Network -> request 'coupon?id=<coupon code>' -> Preview
    PRECONDITIONS: *   To find all details related to the unsuccessfully cashed out coupon open browser console (F12) -> Network -> request 'cashout?Id=<Id>' -> Preview -> betError -> errorDesc (subErrorCode - ?)
    PRECONDITIONS: *   Please see the list of available errors (errorDesc) with corresponding messages that should be shown on the front-end:
    PRECONDITIONS: BET_CANCELLED: "CASHOUT UNAVAILABLE"
    PRECONDITIONS: BET_COMPLETE: "BET SETTLED"
    PRECONDITIONS: BET_LOST: "BET SETTLED"
    PRECONDITIONS: BET_NO_CASHOUT: "CASHOUT UNAVAILABLE"
    PRECONDITIONS: BET_NOT_ACTIVE: "CASHOUT UNAVAILABLE"
    PRECONDITIONS: BET_SETTLED: "BET SETTLED"
    PRECONDITIONS: BET_SUSP: "CASHOUT SUSPENDED"
    PRECONDITIONS: BET_WORTH_NOTHING: "BET HAS NO VALUE"
    PRECONDITIONS: BETTYPE_NO_CASHOUT: CASHOUT UNAVAILABLE"
    PRECONDITIONS: CUST_NO_CASHOUT: CASHOUT UNAVAILABLE"
    PRECONDITIONS: INTERNAL_ERROR: CASHOUT UNAVAILABLE"
    PRECONDITIONS: LEG_NO_CASHOUT: CASHOUT UNAVAILABLE"
    PRECONDITIONS: LEGSORT_NO_CASHOUT: CASHOUT UNAVAILABLE"
    PRECONDITIONS: LINE_NO_CASHOUT: CASHOUT UNAVAILABLE"
    PRECONDITIONS: SELN_NO_CASHOUT: CASHOUT UNAVAILABLE"
    PRECONDITIONS: SELN_NO_COMBI: CASHOUT UNAVAILABLE"
    PRECONDITIONS: SELN_NOT_DISP: CASHOUT UNAVAILABLE"
    PRECONDITIONS: SELN_SUSP: CASHOUT SUSPENDED"
    PRECONDITIONS: SYS_NO_CASHOUT: CASHOUT UNAVAILABLE"
    PRECONDITIONS: When any other error code is received then "CASHOUT UNAVAILABLE" message should be displayed
    PRECONDITIONS: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    """
    keep_browser_open = True

    def test_001__load_sportbook_app_log_in_chose_connect_from_header_ribbon_select_shop_bet_tracker(self):
        """
        DESCRIPTION: * Load Sportbook App
        DESCRIPTION: * Log in
        DESCRIPTION: * Chose 'Connect' from header ribbon
        DESCRIPTION: * Select 'Shop Bet Tracker'
        EXPECTED: Bet Tracker page is opened
        """
        pass

    def test_002_submit_valid_cash_out_code_available_for_cash_out(self):
        """
        DESCRIPTION: Submit valid Cash Out Code available for cash out
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

    def test_004_trigger_situation_when_cash_out_transaction_is_rejectedafter_tapping_confirm_button(self):
        """
        DESCRIPTION: Trigger situation when Cash Out transaction is rejected (after tapping 'CONFIRM' button)
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
        EXPECTED: *   The button text changes to the corresponding error message based on 'betError.errorDesc' attribute in 'cashout' response (see preconditions)
        EXPECTED: *   Button is disabled
        """
        pass

    def test_007_go_to_my_bets__in_shop_bets__sub_tub__repeat_steps_3_6(self):
        """
        DESCRIPTION: Go to 'My Bets' ->'In-Shop Bets'  sub-tub ->
        DESCRIPTION: repeat steps #3-6
        EXPECTED: 
        """
        pass
