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
class Test_C2604124_Coral_Only_Bet_Tracker_page(Common):
    """
    TR_ID: C2604124
    NAME: [Coral Only] Bet Tracker page
    DESCRIPTION: Some test data can be found in spreadsheet (firstly try the last ones, they are the newest):
    DESCRIPTION: https://coralracing-my.sharepoint.com/:x:/g/personal/tetiana_bohdanova_gvcgroup_com/EVgtq0wvD9hMk3cYApkZOhEBkI0G063jRW0YgDUcrv1KZQ?e=b9ZdtC
    DESCRIPTION: if all of them is expired request creating of new coupons (POC - Souparna Datta)
    DESCRIPTION: Info:
    DESCRIPTION: 'In-Shop' - user with card number and pin (The Grid - Ladbrokes; Connect - Coral).
    DESCRIPTION: 'Online' - user with username and password.
    DESCRIPTION: 'Multi-channel' - user who was 'In-Shop' and is upgraded to 'Online' (e.g. has both card#/pin and username/password)
    PRECONDITIONS: 1. Load SportBook App
    PRECONDITIONS: 2. Select Connect from header ribbon
    PRECONDITIONS: 3. Tap 'Shop Bet Tracker'
    PRECONDITIONS: Contact GVC (Venugopal Rao Joshi / Abhinav Goel) and/or Souparna Datta + Oksana Tkach in order to generate In-Shop users
    """
    keep_browser_open = True

    def test_001_verify_bet_tracker_page_when_there_is_no_coupons(self):
        """
        DESCRIPTION: Verify Bet Tracker page when there is no coupons
        EXPECTED: * Back button '< Shop Bet Tracker' redirects user to previous page
        EXPECTED: * Title 'Use coupon code of Bet Receipt number'
        EXPECTED: * '˅' arrow from the right which collapses/ expands text and entry field below (expanded by default)
        EXPECTED: * Text: 'Enter the 7 letter code on Coupon or the long number on your bet receipt. For Betstation bets, you don't need to include the B.'
        EXPECTED: * Entry field and 'Submit' button next to it (inactive when entry field is empty)
        EXPECTED: * Receipt image
        """
        pass

    def test_002_verify_entry_field(self):
        """
        DESCRIPTION: Verify Entry field
        EXPECTED: * Entry field accepts only 7-letters code OR 12-digits code OR 13-digits code, in all other cases error message will be shown 'The coupon code/number entered is incorrect, please try again'
        EXPECTED: * If 7-letters code is entered it's transformed into format XXX-XXXX
        EXPECTED: * More than 13 digits cannot be entered
        """
        pass

    def test_003_log_in_with_in_shop_or_multi_channel_user(self):
        """
        DESCRIPTION: Log in with In-Shop OR Multi channel user
        EXPECTED: User is logged in successfully
        """
        pass

    def test_004_navigate_to_bet_tracker(self):
        """
        DESCRIPTION: Navigate to Bet Tracker
        EXPECTED: * Bet Tracker page is loaded
        """
        pass

    def test_005_verify_correct_request_is_sent_to_retail_bpp_proxi_to_receive_coupons_codes_attached_to_logged_in_user(self):
        """
        DESCRIPTION: Verify correct request is sent to Retail-bpp Proxi to receive coupons codes attached to logged in user
        EXPECTED: * In browser console find 'connect'
        EXPECTED: * In request body parameter 'cardNumber' is populated with Connect card number of logged in user; 'username' is populated with username of logged in user
        EXPECTED: * In response,  'open' and 'settled' sections contain coupons attached to the user
        EXPECTED: * If 'open' and 'settled' sections contain coupons - they are displayed on UI correctly
        """
        pass

    def test_006_verify_bet_tracker_page_with_coupons_codessubmit_some_coupons_manually(self):
        """
        DESCRIPTION: Verify Bet Tracker page with coupons codes
        DESCRIPTION: (Submit some coupons manually)
        EXPECTED: * If user has coupon codes placed via his Connect card than list of coupons is displayed, manually submitted coupons will go first
        EXPECTED: * 'Open bets' and 'Settled bets' tabs are displayed below entry field
        EXPECTED: * Coupons from 'open' section (in console) are displayed on Open bets tabs
        EXPECTED: * Coupons from 'settled 'section (in console) are displayed on Settled bets tabs
        EXPECTED: * Coupons order corresponds to Retail-bpp Proxi response
        """
        pass

    def test_007_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: List of coupons remains the same as in previous step
        """
        pass

    def test_008__navigate_to_my_bets___in_shop_bets_verify_tab_content(self):
        """
        DESCRIPTION: * Navigate to My Bets -> In-Shop bets
        DESCRIPTION: * Verify tab content
        EXPECTED: Tab contains completely the same coupons (in the same order) as in previous step
        """
        pass
