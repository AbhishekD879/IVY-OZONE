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
class Test_C2081357_Verify_unavailable_for_cash_out_coupon_general(Common):
    """
    TR_ID: C2081357
    NAME: Verify unavailable for cash out coupon (general)
    DESCRIPTION: This test case verifies unavailable for cash out coupon
    DESCRIPTION: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    PRECONDITIONS: *   Valid Cash Out Coupon Codes should be generated where cash out option is disabled (support is needed from RCOMB team)
    PRECONDITIONS: *   To find all details related to the coupon open browser console (F12) -> Network -> request 'coupon?id=<coupon code>' -> Preview -> bet -> cashoutValue
    PRECONDITIONS: *   Please see the list of available errors with corresponding messages that should be shown on the front-end:
    PRECONDITIONS: BET_CANCELLED: "CASHOUT UNAVAILABLE"
    PRECONDITIONS: BET_CASHED_OUT: "BET ALREADY CASHED OUT"
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
    PRECONDITIONS: To trigger error you suspend event/market/selection OR make bet settled by finishing events (in Amelco) OR make bet worth nothing by changing price (in Amelco)
    PRECONDITIONS: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    """
    keep_browser_open = True

    def test_001__load_spotbook_app_log_in_chose_connect_from_header_ribbon_tap_shop_bet_tracker_item(self):
        """
        DESCRIPTION: * Load SpotBook App
        DESCRIPTION: * Log in
        DESCRIPTION: * Chose 'Connect' from header ribbon
        DESCRIPTION: * Tap 'Shop Bet Tracker' item
        EXPECTED: Bet Tracker page is opened
        """
        pass

    def test_002_submit_valid_cash_out_code_which_containsselections_not_available_for_cash_out(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains selection(s) NOT available for cash out
        EXPECTED: *   Cash Out Code is submitted successfully
        EXPECTED: *   Cash Out Coupon is shown to the user expanded by default
        """
        pass

    def test_003_verify_cash_out_section_of_added_coupon(self):
        """
        DESCRIPTION: Verify Cash Out section of added coupon
        EXPECTED: *   Disabled border button is shown with corresponding error message (see preconditions)
        EXPECTED: *   Cash Out is not available
        """
        pass

    def test_004_go_to_my_bets__in_shop_bets_sub_tub__repeat_step_3(self):
        """
        DESCRIPTION: Go to 'My Bets' ->'In-Shop Bets' sub-tub ->
        DESCRIPTION: repeat step #3
        EXPECTED: 
        """
        pass
