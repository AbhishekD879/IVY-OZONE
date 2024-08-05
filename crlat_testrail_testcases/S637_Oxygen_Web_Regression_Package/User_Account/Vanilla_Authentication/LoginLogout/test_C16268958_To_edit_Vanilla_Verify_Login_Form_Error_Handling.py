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
class Test_C16268958_To_edit_Vanilla_Verify_Login_Form_Error_Handling(Common):
    """
    TR_ID: C16268958
    NAME: [To edit] [Vanilla] Verify Login Form Error Handling
    DESCRIPTION: 
    PRECONDITIONS: User should not be logged in
    """
    keep_browser_open = True

    def test_001_clicktap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: 'Log in' form is opened
        """
        pass

    def test_002_enter_valid_username_and_invalid_password(self):
        """
        DESCRIPTION: Enter valid username and invalid password
        EXPECTED: Data is entered and displayed
        """
        pass

    def test_003_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log In' button
        EXPECTED: " ! The credentials entered are incorrect " error message appears
        EXPECTED: Password field is highlighted in red
        EXPECTED: "!" icon appears for "Password field"
        """
        pass

    def test_004_enter_invalid_username_and_valid_password(self):
        """
        DESCRIPTION: Enter invalid username and valid password
        EXPECTED: The same result as for "Step3"
        """
        pass

    def test_005_enter_invalid_username_and_invalid_password(self):
        """
        DESCRIPTION: Enter invalid username and invalid password
        EXPECTED: The same result as for "Step3"
        """
        pass
