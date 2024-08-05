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
class Test_C2031550_Verify_Bet_Tracker_page(Common):
    """
    TR_ID: C2031550
    NAME: Verify Bet Tracker page
    DESCRIPTION: This test case verify Bet Tracker home entry screen
    PRECONDITIONS: Make sure Bet Tracker feature is turned on in CMS: System configuration -> Connect -> shop Bet Tracker
    PRECONDITIONS: * Load SpotBook App
    PRECONDITIONS: * Chose 'Connect' from header ribbon -> Connect landing page is opened
    PRECONDITIONS: * Tap 'Shop Bet Tracker' item -> Bet Tracker page is opened
    """
    keep_browser_open = True

    def test_001_verify_bet_tracker_page_structure_when_there_is_no_coupons(self):
        """
        DESCRIPTION: Verify Bet Tracker page structure when there is no coupons
        EXPECTED: * Back button '< In-Shop Bet Tracker' that redirects user to the previous page
        EXPECTED: * 'Use coupon code or Bet Receipt number' title
        EXPECTED: * 'v' arrow next to it that expands/collapses area below
        EXPECTED: * Text: 'Enter the 7 letter code on your Coupon or the long number in your bet receipt. For Betstation bets, you don't need to include the B' (expanded by default)
        EXPECTED: * Entry field  with 'Submit' button next to it
        EXPECTED: * Coupon Receipt image (on grey background)
        """
        pass

    def test_002__verify_bet_tracker_page_structure_when_there_is_some_coupon_available_submit_oneseveral_coupon_codes(self):
        """
        DESCRIPTION: * Verify Bet Tracker page structure when there is some coupon available
        DESCRIPTION: * Submit one/several coupon codes
        EXPECTED: * Tabs 'Open Bets' and 'Settled bets' appears instead of Coupon Receipt image
        EXPECTED: * Coupons are submitted successfully and displayed on 'Open Bets'/ 'Settled bets' accordingly to their settlement status
        """
        pass
