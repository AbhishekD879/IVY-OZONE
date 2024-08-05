import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C2987502_Verify_navigating_to_from_Account_One_portal_Change_Password_page(Common):
    """
    TR_ID: C2987502
    NAME: Verify navigating to/from 'Account One' portal 'Change Password' page
    DESCRIPTION: This test case verifies redirection from 'Roxanne' app to 'Change Password' page on IMS 'Account One' portal via 'Change Password' menu items/links across an app
    DESCRIPTION: AUTOTEST
    DESCRIPTION: Mobile [C16396581]
    DESCRIPTION: Desktop [C16396582]
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

    def test_001_navigate_to_the_my_account___change_password(self):
        """
        DESCRIPTION: Navigate to the 'My account' -> 'Change password'
        EXPECTED: * Account one personal-details page is open
        EXPECTED: * URL corresponds to URL from preconditions
        """
        pass

    def test_002_tap_change_password_tab(self):
        """
        DESCRIPTION: Tap 'Change Password' tab
        EXPECTED: The 'Change Password' tab is open
        """
        pass

    def test_003_fill_in_fields_with_valid_data___tap_close_button_x(self):
        """
        DESCRIPTION: Fill in fields with valid data -> Tap 'Close' button ('X')
        EXPECTED: * User is navigated back to the sportsbook homepage
        EXPECTED: * User is logged in
        """
        pass
