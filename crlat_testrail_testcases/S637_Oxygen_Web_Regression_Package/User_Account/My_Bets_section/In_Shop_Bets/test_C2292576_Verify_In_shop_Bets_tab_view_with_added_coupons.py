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
class Test_C2292576_Verify_In_shop_Bets_tab_view_with_added_coupons(Common):
    """
    TR_ID: C2292576
    NAME: Verify In-shop Bets tab view with added coupons
    DESCRIPTION: This test case verifies Bet History mode on Bet Tracker: In-shop Bets tab with added coupons
    DESCRIPTION: User story: BMA-30953 Bet History mode on Bet Tracker
    PRECONDITIONS: Request creation of following test coupons (some of them should be placed via Connect card and some - anonymously):
    PRECONDITIONS: * OTC (EPOS1 and EPOS2)
    PRECONDITIONS: * SSBT
    PRECONDITIONS: 1. Load SportBook
    PRECONDITIONS: 2. Log in with account that has some in-shop bets placed via his/her Connect Card number
    PRECONDITIONS: 3. Open Connect from header ribbon -> select 'Shop Bet Tracker'
    PRECONDITIONS: 4. Make sure bets (coupons) placed via Connect Card are displayed
    PRECONDITIONS: 5. Add several coupons manually (placed anonymously)
    PRECONDITIONS: 6. Manually added coupons are submitted successfully and added to the top of the coupons list
    """
    keep_browser_open = True

    def test_001_go_to_me_bets___in_shop_bets_tab(self):
        """
        DESCRIPTION: Go to 'Me Bets' -> 'In-Shop Bets' tab
        EXPECTED: 
        """
        pass

    def test_002_verify_structure_of_in_shop_bets_tab(self):
        """
        DESCRIPTION: Verify structure of IN-SHOP BETS tab
        EXPECTED: * 'Open bets' and 'Settled bets' sub-tabs
        """
        pass

    def test_003_verify_content_of_open_bets_tab(self):
        """
        DESCRIPTION: Verify content of 'Open bets' tab
        EXPECTED: * 'Open bets' tab contains the same list of coupons as 'Open bets' tab on 'Shop Bet Tracker' screen
        EXPECTED: * User cannot add new coupons but can delete existing one by 'delete button' (at the top right corner)
        EXPECTED: * Coupons quantity and order correspond to Retail-BPP response (Open dev tool -> Network -> search for 'connect' request -> Preview -> make sure list of displayed coupons corresponds to coupons from 'open' section)
        """
        pass

    def test_004_verify_content_of_settled_bets_tab(self):
        """
        DESCRIPTION: Verify content of 'Settled bets' tab
        EXPECTED: * 'Settled bets' tab contains the same list of coupons as 'Settled bets' tab on 'Shop Bet Tracker' screen
        EXPECTED: * User cannot add AND delete coupons
        EXPECTED: * Coupons quantity and order correspond to Retail-BPP response (Open dev tool -> Network -> search for 'connect' request -> Preview -> make sure list of displayed coupons corresponds to coupons from 'settled' section)
        """
        pass

    def test_005__go_to_shop_bet_tracker_page_delete_several_coupons_on_both_open_bet_and_settled_bet_tabs_submit_several_more_coupons_manually_on_both_open_bet_and_settled_bet_tabs(self):
        """
        DESCRIPTION: * Go to 'Shop Bet Tracker' page
        DESCRIPTION: * Delete several coupons (on both 'Open Bet' and 'Settled bet' tabs)
        DESCRIPTION: * Submit several more coupons manually (on both 'Open Bet' and 'Settled bet' tabs)
        EXPECTED: * Coupons are deleted/ added successfully
        """
        pass

    def test_006__get_back_to_my_bets___in_shop_bets_tab_make_sure_all_changes_made_on_shop_bet_tracker_page_are_mirrored_on_in_shop_bets_tab_correctly(self):
        """
        DESCRIPTION: * Get back to 'My Bets' -> 'In-Shop bets' tab
        DESCRIPTION: * Make sure all changes made on 'Shop Bet Tracker' page are mirrored on 'In-Shop bets' tab correctly
        EXPECTED: 'Open bets' and 'Settled bets' tabs show the same set of coupons as on 'Shop Bet Tracker' page:
        EXPECTED: * Coupons deleted in previous step are not displayed
        EXPECTED: * Coupons added is previous steps are displayed at the top
        """
        pass
