import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C59542845_Verify_error_handling_for_failed_CouponToOutcomeForCoupon(Common):
    """
    TR_ID: C59542845
    NAME: Verify error handling for failed /CouponToOutcomeForCoupon
    DESCRIPTION: This test case verifies error handling for failed /CouponToOutcomeForCoupon on the coupon details page
    PRECONDITIONS: 1. Go to the sports landing page
    PRECONDITIONS: 2. Open Coupon tab (ACCA)
    """
    keep_browser_open = True

    def test_001_open_any_coupon_details_page(self):
        """
        DESCRIPTION: Open any coupon details page
        EXPECTED: Events are displayed
        """
        pass

    def test_002_block_coupontooutcomeforcoupon_request_in_chrome_dev_tools___request_blocking_and_refresh_the_page(self):
        """
        DESCRIPTION: Block CouponToOutcomeForCoupon request in Chrome Dev tools -> Request blocking and refresh the page
        EXPECTED: * "Oops! We are having trouble loading this page. Please check your connection" message is shown
        EXPECTED: * "TRY AGAIN" button is displayed under the error message and is clickable
        """
        pass

    def test_003_unblock_coupontooutcomeforcoupon_request_in_chrome_dev_tools___request_blocking_and_press_on_try_again_button(self):
        """
        DESCRIPTION: Unblock CouponToOutcomeForCoupon request in Chrome Dev tools -> Request blocking and press on 'Try Again' button
        EXPECTED: * CouponToOutcomeForCoupon request is resent
        EXPECTED: * CouponToOutcomeForCoupon request is not failed and CouponToOutcomeForCoupon data is received
        EXPECTED: * Error message and 'Try Again' button are no longer displayed
        """
        pass
