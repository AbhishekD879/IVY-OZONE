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
class Test_C35355699_Forgot_Password(Common):
    """
    TR_ID: C35355699
    NAME: Forgot Password
    DESCRIPTION: This test case verifies Password Reseting
    DESCRIPTION: AUTOTEST
    DESCRIPTION: MOBILE: [C9697779]
    PRECONDITIONS: 1. User with email is registered (email service will be used for password reset)
    PRECONDITIONS: 2. User is logged out
    PRECONDITIONS: 3. Login form should be opened
    """
    keep_browser_open = True

    def test_001_tap_i_forgot_my_password_link(self):
        """
        DESCRIPTION: Tap 'I forgot my Password' link
        EXPECTED: 'Forgotten password' page is opened![](index.php?/attachments/get/111269040)
        """
        pass

    def test_002_enter_a_valid_username___tap_submit(self):
        """
        DESCRIPTION: Enter a valid username -> Tap 'Submit'
        EXPECTED: Login page is shown, "Password reset email sent" message is shown![](index.php?/attachments/get/111269041)
        """
        pass

    def test_003_check_email_box(self):
        """
        DESCRIPTION: Check email box
        EXPECTED: Email "Reset your password"![](index.php?/attachments/get/111269044)
        EXPECTED: from Ladbrokes is received
        """
        pass

    def test_004_follow_instructions_in_the_email(self):
        """
        DESCRIPTION: Follow instructions in the email
        EXPECTED: user is able to set new password
        """
        pass

    def test_005_log_in_to_the_app_with_username_and_the_old_password(self):
        """
        DESCRIPTION: Log in to the app with username and the OLD password
        EXPECTED: User is NOT logged in
        """
        pass

    def test_006_log_in_to_the_app_with_username_and_the_new_password(self):
        """
        DESCRIPTION: Log in to the app with username and the NEW password
        EXPECTED: User is successfully logged in
        """
        pass
