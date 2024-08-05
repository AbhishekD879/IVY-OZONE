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
class Test_C16425274_Vanilla_Log_in_with_new_created_user(Common):
    """
    TR_ID: C16425274
    NAME: [Vanilla] Log in with new created user
    DESCRIPTION: This test case verifies that it is possible to log in using new registered user's data
    PRECONDITIONS: Register new user. Make sure you remembered entered username and password.
    PRECONDITIONS: Choosing the password should include following rules:
    PRECONDITIONS: - A letter
    PRECONDITIONS: - A number
    PRECONDITIONS: - 6 to 20 characters
    PRECONDITIONS: - Must not contain parts of your name or e-mail
    PRECONDITIONS: - Must not contain any of these special characters (‘ “ < > & % )
    PRECONDITIONS: Do not make deposit on the last step of registration.
    """
    keep_browser_open = True

    def test_001_load_vanilla_application(self):
        """
        DESCRIPTION: Load Vanilla application
        EXPECTED: 
        """
        pass

    def test_002_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log In' button
        EXPECTED: Log In pop-up opens
        """
        pass

    def test_003_fill_in_username_and_password_fields_with_data_of_just_registered_user___tap_login_button(self):
        """
        DESCRIPTION: Fill in 'Username' and 'Password' fields with data of just registered user -> Tap 'Login' button
        EXPECTED: - Logging in passed successfully.
        EXPECTED: - "Low balance
        EXPECTED: Your account balance is £0.00. Would you like to deposit?"
        EXPECTED: message is displayed at the bottom.
        """
        pass
