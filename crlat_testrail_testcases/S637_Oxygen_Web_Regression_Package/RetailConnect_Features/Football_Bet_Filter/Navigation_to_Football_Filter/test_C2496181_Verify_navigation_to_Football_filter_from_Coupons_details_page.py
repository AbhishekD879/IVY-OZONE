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
class Test_C2496181_Verify_navigation_to_Football_filter_from_Coupons_details_page(Common):
    """
    TR_ID: C2496181
    NAME: Verify navigation to Football filter from Coupons details page
    DESCRIPTION: AUTOTEST [C9836846]
    PRECONDITIONS: Make sure Football Bet Filter feature is turned on in CMS: System configuration -> Connect -> football Filter
    PRECONDITIONS: following API returns events for applying Football filters on (After navigating to Football Filter search in console: *retailCoupon*):
    PRECONDITIONS: **Coral:**
    PRECONDITIONS: https://sandbox-api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LADb3b4313883004240a754070676e25258
    PRECONDITIONS: **Ladbrokes:**
    PRECONDITIONS: https://one-api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LDabc81dcf931d4f368e3f7ce522197bc7&filter=coupon.%7ctoday%27s%20matches%7c
    PRECONDITIONS: 1. Load SportBook App
    PRECONDITIONS: 2. Open Football landing page
    PRECONDITIONS: 3. Select 'Coupons' tab
    """
    keep_browser_open = True

    def test_001_select_any_couponthat_has_couponsortcode_parameter_equal_to_mrto_find_it_search_coupons_in_console(self):
        """
        DESCRIPTION: Select any coupon
        DESCRIPTION: that has **couponSortCode** parameter equal to "MR"
        DESCRIPTION: (to find it search 'Coupons' in console)
        EXPECTED: Coupons details page is opened
        """
        pass

    def test_002_verify_that_bet_filter_link_is_displayed(self):
        """
        DESCRIPTION: Verify that 'Bet Filter' link is displayed
        EXPECTED: 'Bet Filter' link is placed at the top right corner
        """
        pass

    def test_003_tap_bet_filter_link(self):
        """
        DESCRIPTION: Tap 'Bet Filter' link
        EXPECTED: * Bet Filter page is opened
        EXPECTED: * Proper call to API is made (see precondition), parameter 'filter' is set with selected coupon's name
        """
        pass

    def test_004_tap_find_bets_button(self):
        """
        DESCRIPTION: Tap 'Find bets' button
        EXPECTED: * Result page is displayed and it contains only events that belongs to selected coupons (and events correspond to API response in the same time)
        EXPECTED: * 'Add to Betslip' button at the bottom
        """
        pass

    def test_005_go_back_to_coupons_tab_and_select_any_couponwhere_couponsortcode_parameter_is_not_equal_to_mrto_find_it_search_coupons_in_consoleusually_its_over_under_total_goals(self):
        """
        DESCRIPTION: Go back to 'Coupons' tab and select any coupon
        DESCRIPTION: where **couponSortCode** parameter is NOT equal to "MR"
        DESCRIPTION: (to find it search 'Coupons' in console)
        DESCRIPTION: (Usually it's 'Over/ Under total goals')
        EXPECTED: Coupons details page is opened
        """
        pass

    def test_006_verify_presence_of_bet_filter_link(self):
        """
        DESCRIPTION: Verify presence of 'Bet Filter' link
        EXPECTED: 'Bet Filter' link is absent
        """
        pass
