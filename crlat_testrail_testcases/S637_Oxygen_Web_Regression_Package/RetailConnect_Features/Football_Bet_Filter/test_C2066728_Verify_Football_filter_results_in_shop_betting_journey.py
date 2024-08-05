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
class Test_C2066728_Verify_Football_filter_results_in_shop_betting_journey(Common):
    """
    TR_ID: C2066728
    NAME: Verify Football filter results (in-shop betting journey)
    DESCRIPTION: This test case verifies in-shop betting journey on Football Bet Filter
    PRECONDITIONS: 1. Select 'Connect' from header sports ribbon -> Connect landing page is opened
    PRECONDITIONS: 2. Tap Football Bet Filter -> Bet Filter Page is opened
    """
    keep_browser_open = True

    def test_001_scroll_down_and_tap_find_bets(self):
        """
        DESCRIPTION: Scroll down and tap 'Find Bets'
        EXPECTED: The result page is opened
        """
        pass

    def test_002_check_off_a_few_selections(self):
        """
        DESCRIPTION: Check off a few selections
        EXPECTED: Selections are checked off successfully
        """
        pass

    def test_003_tap_shop_locator_button(self):
        """
        DESCRIPTION: Tap 'SHOP LOCATOR' button
        EXPECTED: A user is redirected to the map with shops
        """
        pass
