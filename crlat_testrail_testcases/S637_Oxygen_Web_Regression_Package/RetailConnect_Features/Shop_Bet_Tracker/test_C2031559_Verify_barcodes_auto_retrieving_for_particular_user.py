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
class Test_C2031559_Verify_barcodes_auto_retrieving_for_particular_user(Common):
    """
    TR_ID: C2031559
    NAME: Verify barcodes auto retrieving for particular user
    DESCRIPTION: This test case verify that only first 10 bets available for the user are displayed firstly, the rest of bets are displayed after tapping 'load more' link
    DESCRIPTION: Jira ticked:
    DESCRIPTION: HMN-2046 Only display first 10 bets in the Connect app retrieved for the user
    PRECONDITIONS: Request OTC (EPOS1 and EPOS2) and SSBT coupon codes assigned to particular user (more than 10 opened and 10 settled coupons should be attached)
    PRECONDITIONS: And coupon codes not assigned to any user
    PRECONDITIONS: Related test case which describe PROXY implementation of this functionality: [Verify SSBT/OpenBet barcodes retrieving via 'connect' endpoint (User History)](https://ladbrokescoral.testrail.com/index.php?/cases/view/1044455)
    PRECONDITIONS: Verify SSBT/OpenBet barcodes retrieving via 'connect' endpoint (User History)
    PRECONDITIONS: Make sure Bet Tracker feature is turned on in CMS: System configuration -> Connect -> shop Bet Tracker
    """
    keep_browser_open = True

    def test_001__load_spotbook_app_log_in_under_user_who_has_some_bets_placed_via_hisher_connect_card_username_otc_and_ssbt(self):
        """
        DESCRIPTION: * Load SpotBook App
        DESCRIPTION: * Log in under user who has some bets placed via his/her connect card/ username (OTC and SSBT)
        EXPECTED: * User is logged in successfully
        """
        pass

    def test_002__chose_connect_from_header_ribbon___connect_landing_page_is_opened_tap_shop_bet_tracker_item(self):
        """
        DESCRIPTION: * Chose 'Connect' from header ribbon -> Connect landing page is opened
        DESCRIPTION: * Tap 'Shop Bet Tracker' item
        EXPECTED: * Bet Tracker page is opened
        EXPECTED: * 'Open Bets' tab is active by default
        EXPECTED: * In browser console: find 'connect' -> verify request body -> parameter 'cardNumber' is populated with Connect card number of logged in user; 'username' is populated with username of logged in user
        """
        pass

    def test_003__verify_open_bets_tab(self):
        """
        DESCRIPTION: * Verify 'Open Bets' tab
        EXPECTED: * First 10 coupons attached to the user are displayed
        EXPECTED: * Coupons are sorted by Bet Creation Date/Time
        EXPECTED: * 'Load more' link is displayed at the bottom of coupons list
        """
        pass

    def test_004_tap_load_more_link_and_verify_result(self):
        """
        DESCRIPTION: Tap 'Load more' link and verify result
        EXPECTED: * Next 10 coupons attached to the user are loaded (or less if there less than 10 remain)
        EXPECTED: * Keep tapping 'Load more'  link until all coupons attached to the user are displayed
        EXPECTED: * When all coupons are loaded 'Load more' link is not displayed any more
        """
        pass

    def test_005_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * First 10 coupons attached to the user are displayed
        """
        pass

    def test_006_go_to_settled_bets_tab_and_repeat_steps_3_5(self):
        """
        DESCRIPTION: Go to 'Settled Bets' tab and repeat steps №3-5
        EXPECTED: 
        """
        pass

    def test_007_go_to_open_bets_tab_and_submit_several_not_settled_coupons_otc_and_ssbt_not_attached_to_the_logged_in_user(self):
        """
        DESCRIPTION: Go to 'Open Bets' tab and submit several not settled coupons (OTC and SSBT) not attached to the logged in user
        EXPECTED: * Coupons are submitted successfully
        EXPECTED: * Coupon are added to the top of the list
        EXPECTED: * Coupons are sorted by sequence they have been submitted
        EXPECTED: * Quantity of displayed coupons is equal to 10 + manually submitted ones
        """
        pass

    def test_008_tap_load_more_link_and_verify_result(self):
        """
        DESCRIPTION: Tap 'Load more' link and verify result
        EXPECTED: * Next 10 coupons attached to the user are loaded (or less if there less than 10 remain)
        EXPECTED: * Quantity of displayed coupons is equal to 20 + manually submitted ones
        """
        pass

    def test_009_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * In total 10 coupons are displayed
        EXPECTED: * Manually added ones go first, sorted by sequence they have been submitted
        EXPECTED: * Coupons attached to the user are going next
        """
        pass

    def test_010_delete_some_manually_added_coupons_and_some_coupons_attached_to_the_user(self):
        """
        DESCRIPTION: Delete some manually added coupons and some coupons attached to the user
        EXPECTED: Coupons are deleted successfully
        """
        pass

    def test_011_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * In total 10 coupons are displayed
        EXPECTED: * Deleted coupons are not displayed any more
        EXPECTED: * Manually added ones go first
        EXPECTED: * Coupons attached to the user are going next
        """
        pass

    def test_012_go_to_settled_bets_tab_and_repeat_steps_7_11_with_settled_coupons(self):
        """
        DESCRIPTION: Go to 'Settled Bets' tab and repeat steps №7-11 with settled coupons
        EXPECTED: 
        """
        pass

    def test_013_verify_that_expired_coupons_codes_are_deleted_from_localstorage(self):
        """
        DESCRIPTION: Verify that expired coupons codes are deleted from LocalStorage
        EXPECTED: 
        """
        pass

    def test_014__submit_several_coupon_codes_then_delete_some_of_them(self):
        """
        DESCRIPTION: * Submit several coupon codes then delete some of them
        EXPECTED: Coupons are submitted/deleted successfully
        """
        pass

    def test_015_open_browser_console___applications___local_storage___httpscoralbettrackercouk(self):
        """
        DESCRIPTION: Open browser console -> Applications -> Local Storage -> https://****coralbettracker.co.uk
        EXPECTED: * Submitted coupons are added to 'Added' sections
        EXPECTED: * Deleted coupons are added to 'Deleted' sections
        """
        pass

    def test_016_wain_until_coupons_from__previous_step_get_expired_that_takes_about_24_h_after_event_start_time(self):
        """
        DESCRIPTION: Wain until coupons from  previous step get expired (that takes about 24 h after Event Start Time)
        EXPECTED: Expired coupons are deleted from Local Storage (deleting occurring after page reloading)
        EXPECTED: **! Tip:**
        EXPECTED: To test step #15 faster just enter manually  not existing coupons codes into 'Added' and 'Deleted'  section of Local Storage --> refresh the page --> not existing coupons are removed from Local Storage
        """
        pass

    def test_017_open_my_bets___in_shop_bets_tap(self):
        """
        DESCRIPTION: Open 'My Bets' -> 'In-Shop bets' tap
        EXPECTED: * Tab is opened and it contains completely the same set of coupons as on 'Shop Bet Tracker' page
        EXPECTED: * In browser console: find 'connect' -> verify request body -> parameter 'cardNumber' is populated with Connect card number of logged in user; 'username' is populated with username of logged in user
        """
        pass
