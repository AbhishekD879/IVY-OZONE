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
class Test_C60004596_Verify_error_handling_for_failed_EventToOutcomeForEvent(Common):
    """
    TR_ID: C60004596
    NAME: Verify error handling for failed /EventToOutcomeForEvent
    DESCRIPTION: This test case verifies error handling for failed /EventToOutcomeForEvent on the coupon details page
    PRECONDITIONS: Go to the sports landing page
    PRECONDITIONS: Open Coupon tab (ACCA)
    """
    keep_browser_open = True

    def test_001_open_any_coupon_details_page(self):
        """
        DESCRIPTION: Open any coupon details page
        EXPECTED: Events are displayed
        """
        pass

    def test_002_block_eventtooutcomeforevent_request_in_chrome_dev_tools__gt_request_blocking_and_refresh_the_page(self):
        """
        DESCRIPTION: Block EventToOutcomeForEvent request in Chrome Dev tools -&gt; Request blocking and refresh the page
        EXPECTED: - 'Oops! We are having trouble loading this page. Please check your connection' message with "TRY AGAIN" buttons are displayed
        """
        pass

    def test_003_unblock_eventtooutcomeforevent_request_in_chrome_dev_tools__gt_request_blocking_and_refresh_the_page(self):
        """
        DESCRIPTION: Unblock EventToOutcomeForEvent request in Chrome Dev tools -&gt; Request blocking and refresh the page
        EXPECTED: - EventToOutcomeForEvent request is resent
        EXPECTED: - EventToOutcomeForEvent request is not failed and
        EXPECTED: - EventToOutcomeForEvent data is received
        EXPECTED: - 'Oops! We are having trouble loading this page. Please check your connection' message with "TRY AGAIN" buttons are no longer displayed
        EXPECTED: - Events loaded and displayed on the page
        """
        pass
