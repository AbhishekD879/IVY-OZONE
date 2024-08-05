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
class Test_C2161210_Verify_footer_of_Football_Filter_Results_page_depending_on_In_Shop_Online_betting_journey(Common):
    """
    TR_ID: C2161210
    NAME: Verify footer of Football Filter Results page depending on In-Shop/ Online betting journey
    DESCRIPTION: This test case verify differences of Football Filter Results page depending on selected betting journey: online or in-shop
    DESCRIPTION: Only footer looks different, the rest is the same
    DESCRIPTION: [Bet Types](https://confluence.egalacoral.com/display/SPI/Bet+Types)
    DESCRIPTION: [Work Around for calculating payout potential of Multiple Bet Types](https://confluence.egalacoral.com/display/SPI/Work+Around+for+calulating+payout+potential+of+Multiple+Bet+Types)
    PRECONDITIONS: 1. Open Football -> Coupons tab -> Select any coupon that has couponSortCode parameter equal to "MR"
    PRECONDITIONS: 2. Tap Football Bet Filter
    PRECONDITIONS: 3. Scroll down and tap 'Find Bets'
    """
    keep_browser_open = True

    def test_001_verify_football_filter_results_page_for_online_betting_journey(self):
        """
        DESCRIPTION: Verify Football Filter Results page for online betting journey:
        EXPECTED: 
        """
        pass

    def test_002_verify_football_filter_results_footer(self):
        """
        DESCRIPTION: Verify 'Football filter results' footer
        EXPECTED: Footer contains:
        EXPECTED: - '£10 bet pays' label and estimated returns are represented as '-' next to it
        EXPECTED: - 'Maximum payout is £1,000,000' text
        EXPECTED: - 'ADD TO BETSLIP' button (inactive until at least one selection is selected)
        """
        pass

    def test_003_check_off_one_several_selections(self):
        """
        DESCRIPTION: Check off one/ several selections
        EXPECTED: * Bets type is displayed correctly and corresponds to quantity of selected selections
        EXPECTED: * Calculated Odds (next to bet type) are displayed correctly and corresponds to Odds of selected selections
        EXPECTED: * '£10 bet pays' label and calculated estimated returns next to it
        EXPECTED: * 'ADD TO BETSLIP' button is active
        """
        pass

    def test_004_verify_football_filter_results_page_for_in_shop_betting_journeyhomepage___select_connect_from_header_sports_ribbon___tap_football_bet_filter___scroll_down___tap_find_bets(self):
        """
        DESCRIPTION: Verify Football Filter Results page for in-shop betting journey:
        DESCRIPTION: Homepage -> Select 'Connect' from header sports ribbon -> Tap Football Bet Filter -> Scroll down -> tap 'Find Bets'
        EXPECTED: 
        """
        pass

    def test_005_verify_football_filter_results_footer(self):
        """
        DESCRIPTION: Verify 'Football filter results' footer
        EXPECTED: Footer contains:
        EXPECTED: - '£10 bet pays' label and estimated returns are represented as '-' next to it
        EXPECTED: - 'Maximum payout is £1,000,000' text
        EXPECTED: - 'Place your bet in any Coral shop and track your bet with Bet Tracker. Odds may vary in-shop.' text
        EXPECTED: - 'SHOP LOCATOR' button (inactive until at least one selection is selected)
        """
        pass

    def test_006_check_off_one_several_selections(self):
        """
        DESCRIPTION: Check off one/ several selections
        EXPECTED: * Bets type is displayed correctly and corresponds to quantity of selected selections
        EXPECTED: * Calculated Odds (next to bet type) are displayed correctly and corresponds to Odds of selected selections
        EXPECTED: * '£10 bet pays' label and calculated estimated returns next to it
        EXPECTED: * 'SHOP LOCATOR' button is active
        """
        pass
