import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C2989424_Verify_navigation_to_from_Account_One_portal_Personal_Details(Common):
    """
    TR_ID: C2989424
    NAME: Verify navigation to/from 'Account One' portal 'Personal Details'
    DESCRIPTION: This test case verifies redirection from 'Roxanne' app to 'Personal Detail' page on IMS 'Account One' portal via 'Personal Detail' menu items/links across an app
    PRECONDITIONS: 1. In CMS > System Configuration > Structure: 'ExternalUrls' section with 'Field Name' = 'my account' & 'Field Value' = [account one url e.g. http://accountone-test.ladbrokes.com/personal-details] is available
    PRECONDITIONS: 2. Roxanne app is loaded
    PRECONDITIONS: 3. User is logged into an app
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link & creds to Ladbrokes IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: * Account One redirection urls:
    PRECONDITIONS: * TST2: http://accountone-test.ladbrokes.com/personal-details?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * STG: https://accountone-stg.ladbrokes.com/personal-details?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * PROD: http://accountone.ladbrokes.com/personal-details?clientType=sportsbook&back_url=[url to an app]
    """
    keep_browser_open = True

    def test_001_mobiletablettap_on_the_balance_in_the_top_right_hand_corner__personal_details_menu_itemdesktopclick_on_my_account_in_the_top_right_hand_corner__personal_details_menu_item(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on the 'Balance' in the top right-hand corner > 'Personal Details' menu item
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Click on 'My Account' in the top right-hand corner > 'Personal Details' menu item
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Personal Details' page
        EXPECTED: **Desktop**
        EXPECTED: 'Account One' portal > 'Personal Details' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_002_tap_on_close_button_x(self):
        """
        DESCRIPTION: Tap on 'Close' button ('X')
        EXPECTED: * User is navigated back to the same page of an app from where he was redirected
        EXPECTED: * User remains logged in
        """
        pass

    def test_003_repeat_step_1(self):
        """
        DESCRIPTION: Repeat Step 1
        EXPECTED: 
        """
        pass

    def test_004___in_account_one_make_some_changes_for_change_address_tab__tap_on_update_button__tap_on_close_button_x(self):
        """
        DESCRIPTION: - In 'Account One': Make some changes for 'Change Address' tab > Tap on 'Update' button
        DESCRIPTION: - Tap on 'Close' button ('X')
        EXPECTED: * User is navigated back to the same page of an app from where he was redirected
        EXPECTED: * User remains logged in
        """
        pass
