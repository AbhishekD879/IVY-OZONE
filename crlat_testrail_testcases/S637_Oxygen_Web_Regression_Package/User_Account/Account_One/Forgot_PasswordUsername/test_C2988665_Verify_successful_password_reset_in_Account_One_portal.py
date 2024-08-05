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
class Test_C2988665_Verify_successful_password_reset_in_Account_One_portal(Common):
    """
    TR_ID: C2988665
    NAME: Verify successful password reset in 'Account One' portal
    DESCRIPTION: This test case verifies successful reset password procedure
    DESCRIPTION: AUTOTEST
    DESCRIPTION: MOBILE: [C9697779]
    PRECONDITIONS: 1. In CMS > System Configuration > Structure: 'ExternalUrls' section with 'Field Name' = 'my account' & 'Field Value' = [account one url e.g. http://accountone-test.ladbrokes.com/forgot-password] is available
    PRECONDITIONS: 2. Roxanne app is loaded
    PRECONDITIONS: 3. User is logged out
    PRECONDITIONS: 4. Login form should be opened
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link & creds to Ladbrokes IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: * Account One redirection urls:
    PRECONDITIONS: * TST2: http://accountone-test.ladbrokes.com/forgot-password?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * STG: https://accountone-stg.ladbrokes.com/forgot-password?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * PROD: http://accountone.ladbrokes.com/forgot-password?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: Account one page for the password resetting is configurable in CMS:
    PRECONDITIONS: Prod
    PRECONDITIONS: https://accountone.ladbrokes.com/forgot-password?clientType=sportsbook&back_url=https%3A%2F%2Fm.ladbrokes.com%2Fen%2F%0A%0A
    PRECONDITIONS: (Stg: http://accountone-stg.ladbrokes.com/ ...
    PRECONDITIONS: TST: http://accountone-test.ladbrokes.com/ ...)
    """
    keep_browser_open = True

    def test_001_tap_forgot_login_details_link(self):
        """
        DESCRIPTION: Tap 'Forgot Login Details' link
        EXPECTED: Account one 'Forgot Login Details' page is open
        """
        pass

    def test_002_in_account_one_enter_a_valid_username_email_date_of_birth___tap_reset_password_button(self):
        """
        DESCRIPTION: In 'Account One': Enter a valid username, email, date of birth -> Tap 'Reset Password' button
        EXPECTED: 'Account One' Page 'A temporary password is sent to {email}' is open
        """
        pass

    def test_003_tap_on_close_button_x(self):
        """
        DESCRIPTION: Tap on 'Close' button (X)
        EXPECTED: User is navigated back to the same page of Roxanne app from where he was redirected
        """
        pass

    def test_004_tap_log_in__enter_the_old_credentials__tap_on_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log In' > enter the old credentials > Tap on 'Log In' button
        EXPECTED: Login is unsuccessful
        """
        pass

    def test_005_repeat_steps_1___2(self):
        """
        DESCRIPTION: Repeat Steps 1 - 2
        EXPECTED: 
        """
        pass

    def test_006_check_email_box(self):
        """
        DESCRIPTION: Check email box
        EXPECTED: Email from Ladbrokes is received. A new password is provided in the email.
        EXPECTED: **NOTE: Password is successfully received only against 'Account One' PROD
        """
        pass

    def test_007_enter_received_temporary_password__tap_continue(self):
        """
        DESCRIPTION: Enter received 'Temporary Password' > Tap 'Continue'
        EXPECTED: User is navigated back to the same page of Roxanne app from where he was redirected
        """
        pass

    def test_008_log_in_to_the_app_with_username_and_new_password(self):
        """
        DESCRIPTION: Log in to the app with username and new password
        EXPECTED: User is successfully logged in
        """
        pass
