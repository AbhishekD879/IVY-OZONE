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
class Test_C2069259_Verify_Complete_label_displaying_for_coupons_with_several_selections_available_for_cash_out(Common):
    """
    TR_ID: C2069259
    NAME: Verify 'Complete' label displaying for coupons with several selections available for cash out
    DESCRIPTION: This test case verifies 'Complete' label displaying for coupons with several selections available for cah out
    PRECONDITIONS: Valid Multiple Cash Out Coupon Code (that contains several bets in it) should be generated (support is needed from RCOMB team)
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

    def test_002_submit_valid_cash_out_code_which_containseveralselections_single_or_multiple_available_for_cash_out(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contain **several **selections (single or multiple) available for cash out
        EXPECTED: *   Cash Out Code is submitted successfully
        EXPECTED: *   Cash Out Coupon is shown to the user expanded by default
        """
        pass

    def test_003_cash_out_one_of_the_selections_available_for_cash_out(self):
        """
        DESCRIPTION: Cash out one of the selections available for cash out
        EXPECTED: *   Selection is successfully cashed out
        EXPECTED: *   Coupon code is not settled yet
        EXPECTED: *   '(Complete)' label is not added to coupon header
        """
        pass

    def test_004_cash_out_all_selections_available_for_cash_out_within_added_coupon(self):
        """
        DESCRIPTION: Cash out all selections available for cash out within added coupon
        EXPECTED: *   All selections are cashed out successfully
        EXPECTED: *   '(Complete)' label is added to the coupon header
        EXPECTED: *   Coupon code is settled
        """
        pass

    def test_005_go_to_my_bets__in_shop_bets__sub_tub__repeat_steps_3_4(self):
        """
        DESCRIPTION: Go to 'My Bets' ->'In-Shop Bets'  sub-tub ->
        DESCRIPTION: repeat steps #3-4
        EXPECTED: 
        """
        pass
