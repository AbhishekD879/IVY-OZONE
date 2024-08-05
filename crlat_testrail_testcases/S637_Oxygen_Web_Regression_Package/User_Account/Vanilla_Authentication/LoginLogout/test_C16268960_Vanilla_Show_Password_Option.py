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
class Test_C16268960_Vanilla_Show_Password_Option(Common):
    """
    TR_ID: C16268960
    NAME: [Vanilla] Show Password Option
    DESCRIPTION: This test case verifies 'Show password' option
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log in' button
        EXPECTED: 'Log In' pop-up appears
        """
        pass

    def test_002_verify_show_icon(self):
        """
        DESCRIPTION: Verify 'Show' icon
        EXPECTED: 'Show' icon is shown within Password input field
        """
        pass

    def test_003_fill_in_username_and_password_fields_with_valid_login_and_password(self):
        """
        DESCRIPTION: Fill in 'Username' and 'Password' fields with valid login and password
        EXPECTED: *   Valid login and password are entered
        EXPECTED: *   Password is hidden from user, displaying dots
        """
        pass

    def test_004_tap_on_show_icon(self):
        """
        DESCRIPTION: Tap on 'Show' icon
        EXPECTED: *   'Show' inscription changes by 'Hide' on button/icon
        EXPECTED: *   Password is not hidden anymore
        EXPECTED: *   User is able to see characters typed in 'Password' field
        """
        pass

    def test_005_verify_correctness_of_password(self):
        """
        DESCRIPTION: Verify correctness of password
        EXPECTED: Displayed password corresponds to password entered on step #4
        """
        pass

    def test_006_clicktap_on_hide_buttonicon(self):
        """
        DESCRIPTION: Click/Tap on 'Hide' button/icon
        EXPECTED: *   'Hide' inscription changes by 'Show' on button/icon
        EXPECTED: *   Password is hidden from user again
        """
        pass
