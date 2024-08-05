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
class Test_C2031551_Verify_Open_bets_Settled_bets_tabs_on_Bet_Tracker_page(Common):
    """
    TR_ID: C2031551
    NAME: Verify Open bets/ Settled bets tabs on Bet Tracker page
    DESCRIPTION: This test case verify Open bets/ Settled bets tabs for Bet Tracker
    PRECONDITIONS: Request creation of following barcodes:
    PRECONDITIONS: * OTC (EPOS1 and EPOS2)
    PRECONDITIONS: * SSBT
    PRECONDITIONS: ___________________________________________
    PRECONDITIONS: Make sure Bet Tracker feature is turned on in CMS: System configuration -> Connect -> shop Bet Tracker
    PRECONDITIONS: * Load SpotBook App
    PRECONDITIONS: * Chose 'Connect' from header ribbon -> Connect landing page is opened
    PRECONDITIONS: * Tap 'Shop Bet Tracker' item -> Bet Tracker page is opened
    """
    keep_browser_open = True

    def test_001_submit_not_settled_coupons_code(self):
        """
        DESCRIPTION: Submit not settled coupons code
        EXPECTED: * 'Open bets' tab becomes active
        EXPECTED: * Coupon is submitted successfully to the 'Open bets' tab
        """
        pass

    def test_002_submit_settled_coupons_code(self):
        """
        DESCRIPTION: Submit settled coupons code
        EXPECTED: * 'Settled bets'  becomes active
        EXPECTED: * Coupon is submitted successfully to the 'Settled bets' tab
        """
        pass

    def test_003_submit_several_more_settled_and_unsettled_coupons(self):
        """
        DESCRIPTION: Submit several more settled and unsettled coupons
        EXPECTED: * Unsettled coupons are added to the 'Open bets' tab
        EXPECTED: * Settled coupons are added to the 'Settled bets' tab
        EXPECTED: * Each time tab where coupon was added is becoming active
        EXPECTED: * Coupons are ordered by sequence they have been added, recently added ones go first
        """
        pass

    def test_004_go_to_open_bets_tab_and_cash_out_one_of_coupons(self):
        """
        DESCRIPTION: Go to 'Open bets' tab and Cash out one of coupons
        EXPECTED: * Bet is cashed out successfully
        EXPECTED: * Bet is moved to 'Settled bets' tab
        """
        pass

    def test_005_go_to_open_bets_tab_and_trigger_bet_settlement_for_one_of_coupons_e_g_finish_all_events(self):
        """
        DESCRIPTION: Go to 'Open bets' tab and trigger bet settlement for one of coupons (e. g.: finish all events)
        EXPECTED: * After bet gets settled it is moved to 'Settled bets' tab
        """
        pass

    def test_006_submit_multiple_coupon_that_contains_several_open_bets(self):
        """
        DESCRIPTION: Submit multiple coupon that contains several open bets
        EXPECTED: Coupon is submitted successfully to the 'Open bets' tab
        """
        pass

    def test_007_cash_out_one_of_the_multiple_coupons_bet(self):
        """
        DESCRIPTION: Cash out one of the multiple coupon's bet
        EXPECTED: * Bet is cashed out successfully
        EXPECTED: * Coupon remains on the 'Open bets' tab until all coupons bets are settled
        """
        pass

    def test_008_trigger_bet_settlement_for_the_rest_of_multiple_coupons_bet(self):
        """
        DESCRIPTION: Trigger bet settlement for the rest of multiple coupon's bet
        EXPECTED: * All bets are settled successfully
        EXPECTED: * Coupon is moved to 'Settled bets' tab once last bet became settled
        """
        pass

    def test_009_verify_that_all_manually_submitted_coupons_will_be_displayed_after__page_reloading_re_navigation_to_bet_tracker_page(self):
        """
        DESCRIPTION: Verify that all manually submitted coupons will be displayed after  page reloading/ re-navigation to Bet Tracker page
        EXPECTED: * All coupons submitted in previous steps are displayed (until they are expired or deleted)
        """
        pass
