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
class Test_C2989459_Verify_navigating_to_from_Account_One_portal_Forgot_Login_Details_page(Common):
    """
    TR_ID: C2989459
    NAME: Verify navigating to/from 'Account One' portal 'Forgot Login Details' page
    DESCRIPTION: This test case verifies redirection from 'Roxanne' app to 'Reset Password' page on IMS 'Account One' portal via 'Forgot Login Details?' link on login pop-up
    PRECONDITIONS: 1. In CMS > System Configuration > Structure: 'ExternalUrls' section with 'Field Name' = 'my account' & 'Field Value' = [account one url e.g. http://accountone-test.ladbrokes.com/forgot-password] is available
    PRECONDITIONS: 2. Roxanne app is loaded
    PRECONDITIONS: 3. User is logged out
    PRECONDITIONS: 4. Login pop-up is opened
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link & creds to Ladbrokes IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: * Account One redirection urls:
    PRECONDITIONS: * TST2: http://accountone-test.ladbrokes.com/forgot-password?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * STG: https://accountone-stg.ladbrokes.com/forgot-password?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * PROD: http://accountone.ladbrokes.com/forgot-password?clientType=sportsbook&back_url=[url to an app]
    """
    keep_browser_open = True

    def test_001_tap_forgot_login_details_link(self):
        """
        DESCRIPTION: Tap 'Forgot Login Details?' link
        EXPECTED: User is redirected to 'Account One' portal > 'Forgot Login Details?' > 'Reset Password' page
        """
        pass

    def test_002_tap_close_button_x(self):
        """
        DESCRIPTION: Tap 'Close' button (X)
        EXPECTED: User is navigated back to the same page of an app from where he was redirected
        """
        pass

    def test_003_open_login_popup_and__tap_forgot_login_details_link(self):
        """
        DESCRIPTION: Open Login popup and > Tap 'Forgot Login Details?' link
        EXPECTED: User is redirected to 'Account One' portal > 'Forgot Login Details?' > 'Reset Password' page
        """
        pass

    def test_004_enter_valid_username_email_by_default_its_testplaytechcom_birth_date_and_tap_reset_password_button(self):
        """
        DESCRIPTION: Enter valid username, email (by default it's test@playtech.com), birth date and tap Reset Password button
        EXPECTED: Temporary password is set, success message displayed
        """
        pass

    def test_005_tap_close_button_x(self):
        """
        DESCRIPTION: Tap 'Close' button (X)
        EXPECTED: User is navigated back to the same page of an app from where he was redirected
        """
        pass

    def test_006_tap_log_in__enter_valid_credentials__tap_on_log_in_buttonin_order_to_set_new_password_please_navigate_to_account_one_ladbrokes_ims_and_search_user_for_which_youve_done_password_reset(self):
        """
        DESCRIPTION: Tap 'Log In' > enter valid credentials > Tap on 'Log In' button
        DESCRIPTION: (In order to set new password please navigate to Account One Ladbrokes IMS and search user for which you've done password reset)
        EXPECTED: User is successfully logged in
        """
        pass
