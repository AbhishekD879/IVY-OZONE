import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C2297618_Verify_In_shop_Bets_tab_lazy_loading(Common):
    """
    TR_ID: C2297618
    NAME: Verify In-shop Bets tab lazy loading
    DESCRIPTION: This test case verifies that only first 10 bets available for the user are displayed firstly, the rest of bets are displayed after tapping 'load more' link
    PRECONDITIONS: Request creation of following test coupons (some of them should be placed via Connect card and some - anonymously):
    PRECONDITIONS: * OTC (EPOS1 and EPOS2)
    PRECONDITIONS: * SSBT
    PRECONDITIONS: Load SportBook
    PRECONDITIONS: Log in with account that has some in-shop bets placed via his/her Connect Card number
    PRECONDITIONS: Open Connect from header ribbon -> select 'Shop Bet Tracker'
    PRECONDITIONS: Make sure bets (coupons) placed via Connect Card are displayed
    PRECONDITIONS: Add several coupons manually (placed anonymously)
    PRECONDITIONS: Manually added coupons are submitted successfully and added to the top of the coupons list (make sure that all together you have more than 10 coupons on 'Open Bets' and more than 10 coupons on 'Settled' bets tabs)
    PRECONDITIONS: Go to 'Me Bets' -> 'In-Shop Bets' tab
    """
    keep_browser_open = True

    def test_001_open_in_shop_bets_tab(self):
        """
        DESCRIPTION: Open 'In shop bets' tab
        EXPECTED: * 'Open Bets' sub-tab is active
        EXPECTED: * First 10 coupons attached to the user are displayed
        """
        pass

    def test_002_verify_load_more_link_is_displayed_on_open_bets_tab_when_user_has_more_than_10_coupons_attached(self):
        """
        DESCRIPTION: Verify 'Load more' link is displayed on 'Open Bets' tab when user has more than 10 coupons attached
        EXPECTED: * Open dev tool -> Network -> search for 'connect' request -> Preview -> make sure list of displayed coupons corresponds to coupons from 'open' section
        EXPECTED: * Parameter 'total' contains value higher than quantity of displayed coupons
        """
        pass

    def test_003_tap_load_more_link(self):
        """
        DESCRIPTION: Tap 'Load more' link
        EXPECTED: * Next 10 (or less) coupons are loaded
        EXPECTED: * 'Load more' links is displayed until quantity of displayed coupons is equal to 'total' parameter
        """
        pass

    def test_004_verify_load_more_link_is_displayed_on_settled_bets_tab_when_user_has_more_than_10_coupons_attached(self):
        """
        DESCRIPTION: Verify 'Load more' link is displayed on 'Settled Bets' tab when user has more than 10 coupons attached
        EXPECTED: * Open dev tool -> Network -> search for 'connect' request -> Preview -> make sure list of displayed coupons corresponds to coupons from 'settled' section
        EXPECTED: * Parameter 'total' contains value higher than quantity of displayed coupons
        """
        pass

    def test_005_tap_load_more_link(self):
        """
        DESCRIPTION: Tap 'Load more' link
        EXPECTED: * Next 10 (or less) coupons are loaded
        EXPECTED: * 'Load more' links is displayed until quantity of displayed coupons is equal to 'total' parameter
        """
        pass

    def test_006_refresh_page_or_re_navigate_to_in_shop_bets_tab(self):
        """
        DESCRIPTION: Refresh page OR re-navigate to 'In-Shop Bets' tab
        EXPECTED: * 'Open Bets' sub-tab shows first open 10 coupons attached to the user
        EXPECTED: * 'Settled Bets' sub-tab shows first settled 10 coupons attached to the user
        """
        pass
