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
class Test_C36407021_Forgot_Username(Common):
    """
    TR_ID: C36407021
    NAME: Forgot Username
    DESCRIPTION: This test case verifies successful reminding of username
    PRECONDITIONS: User with valid (real) email should be registered.
    PRECONDITIONS: Note: User can use 'Forgot username?' feature ONLY once a day.
    PRECONDITIONS: For verification valid email can be set to already registered user in Account menu -> Settings -> My Account Details
    PRECONDITIONS: * User is Logged Out
    """
    keep_browser_open = True

    def test_001_clicktap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: 'Log in' pop-up appears
        """
        pass

    def test_002_clicktap_on_i_forgot_my_username(self):
        """
        DESCRIPTION: Click/Tap on 'I forgot my Username'
        EXPECTED: 'Forgotten Username' page is opened
        EXPECTED: ![](index.php?/attachments/get/111269048)
        """
        pass

    def test_003_enter_valid_email_and_date_of_birth_into_corresponding_fields(self):
        """
        DESCRIPTION: Enter valid email and date of birth into corresponding fields
        EXPECTED: 
        """
        pass

    def test_004_clicktap_submit_button(self):
        """
        DESCRIPTION: Click/Tap 'Submit' button
        EXPECTED: * 'Log in' pop-up is opened
        EXPECTED: * Success Message is displayed:
        EXPECTED: - Your User Id was sent to your email
        EXPECTED: Please check you email to obtain it.
        EXPECTED: ![](index.php?/attachments/get/111269052)
        """
        pass

    def test_005_check_email_inbox(self):
        """
        DESCRIPTION: Check Email inbox
        EXPECTED: An email with Username from Ladbrokes is received
        EXPECTED: ![](index.php?/attachments/get/111269053)
        """
        pass

    def test_006_go_back_to_applicationlogin_with_received_username(self):
        """
        DESCRIPTION: Go back to application
        DESCRIPTION: Login with received username
        EXPECTED: User is logged in successfully with reminded username
        """
        pass
