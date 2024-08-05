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
class Test_C2069263_Verify_OTC_NON_Cash_Out_coupon_code_for_Football(Common):
    """
    TR_ID: C2069263
    NAME: Verify OTC NON Cash Out coupon code for Football
    DESCRIPTION: This test case verify coupon codes view in General
    DESCRIPTION: Bets can be placed on any sport so
    DESCRIPTION: please note that there is 3 different design only for 3 sports: Football, Tennis and Racing,
    DESCRIPTION: if there is coupon that contains bet placed on any other sport except Football, Tennis and Racing then Football design will be applied
    PRECONDITIONS: *   Valid Cash Out Coupon Code should be generated (support is needed from RCOMB team)
    PRECONDITIONS: *   To find all details related to the coupon open browser console (F12) -> Network -> request 'coupon?id=<coupon code>' -> Preview
    PRECONDITIONS: *   To find details about date and time of bet placement in Preview tab of 'coupon?id=<coupon code>' request expand the following elements: bet -> timeStamp
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

    def test_002_submit_valid_non_cash_out_code(self):
        """
        DESCRIPTION: Submit valid NON Cash Out Code
        EXPECTED: *   Cash Out Code is submitted successfully
        EXPECTED: *   Cash Out Coupon is shown to the user expanded by default
        EXPECTED: *   It is possible to collapse/expand coupon section
        EXPECTED: *   All associated bets are shown within the coupon
        """
        pass

    def test_003_verify_presence_of_cash_out_functionality(self):
        """
        DESCRIPTION: Verify presence of Cash Out functionality
        EXPECTED: Cash Out button is not displayed for NON Cash Out coupons
        EXPECTED: (the rest is completely the same as for Cash out coupons)
        """
        pass

    def test_004_go_to_my_bets__in_shop_bets__sub_tub__repeat_step_3(self):
        """
        DESCRIPTION: Go to 'My Bets' ->'In-Shop Bets'  sub-tub ->
        DESCRIPTION: repeat step #3
        EXPECTED: 
        """
        pass
