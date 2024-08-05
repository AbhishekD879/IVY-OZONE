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
class Test_C2987524_Verify_successful_Password_Changing(Common):
    """
    TR_ID: C2987524
    NAME: Verify successful Password Changing
    DESCRIPTION: This test case verifies successful password changing
    DESCRIPTION: AUTOTEST
    DESCRIPTION: Mobile [C16268836]
    DESCRIPTION: Desktop [C15830105]
    PRECONDITIONS: 1. In CMS > System Configuration > Structure: 'ExternalUrls' section with 'Field Name' = 'personal-details' & 'Field Value' = [account one url e.g. http://accountone-test.ladbrokes.com/personal-details] is available
    PRECONDITIONS: 2. Roxanne app is loaded
    PRECONDITIONS: 3. User is logged into an app
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link & creds to Ladbrokes IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: Account One redirection URLs:
    PRECONDITIONS: TST2: http://accountone-test.ladbrokes.com/personal-details?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: STG: https://accountone-stg.ladbrokes.com/personal-details?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: PROD: http://accountone.ladbrokes.com/personal-details?clientType=sportsbook&back_url=[url to an app]
    """
    keep_browser_open = True

    def test_001_navigate_to_the_my_account__personal_detailsormy_account__change_password(self):
        """
        DESCRIPTION: Navigate to the 'My account' > 'Personal Details'
        DESCRIPTION: OR
        DESCRIPTION: 'My account' > 'Change password'
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

    def test_003_fill_in_fields_with_valid_data__tap_submit(self):
        """
        DESCRIPTION: Fill in fields with valid data > Tap 'Submit'
        EXPECTED: Message 'Successfully changed' appears
        """
        pass

    def test_004_tap_close_button_x(self):
        """
        DESCRIPTION: Tap Close button (X)
        EXPECTED: * User is navigated back to the sportsbook homepage
        EXPECTED: * User is logged in
        """
        pass

    def test_005_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is successfully logged out
        """
        pass

    def test_006_log_in_with_the_old_password(self):
        """
        DESCRIPTION: Log in with the old password
        EXPECTED: It is impossible to log in with the old password
        """
        pass

    def test_007_log_in_with_the_new_password(self):
        """
        DESCRIPTION: Log in with the new password
        EXPECTED: User is logged in successfully with the new password
        """
        pass
