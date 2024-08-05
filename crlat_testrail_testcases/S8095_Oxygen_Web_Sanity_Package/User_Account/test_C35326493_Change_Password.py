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
class Test_C35326493_Change_Password(Common):
    """
    TR_ID: C35326493
    NAME: Change Password
    DESCRIPTION: This test case verifies 'Change Password' functionality
    DESCRIPTION: AUTOTEST [C45122678]
    PRECONDITIONS: Choosing the password should include following rules:
    PRECONDITIONS: At least 8 characters;
    PRECONDITIONS: Uppercase and lowercase letters;
    PRECONDITIONS: Numbers and symbols
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_with_valid_credentials(self):
        """
        DESCRIPTION: Log in with valid credentials
        EXPECTED: * User is successfully logged in
        """
        pass

    def test_003_clicktap_on_my_account_menu_on_the_header(self):
        """
        DESCRIPTION: Click/Tap on 'My Account' Menu on the Header
        EXPECTED: 'My Account' menu is displayed
        EXPECTED: ![](index.php?/attachments/get/14054191)
        """
        pass

    def test_004_clicktap_on_settings____change_password_menu_item(self):
        """
        DESCRIPTION: Click/Tap on 'Settings' --> 'Change Password' menu item
        EXPECTED: 'Change Password' page is opened
        EXPECTED: ![](index.php?/attachments/get/14054197)
        """
        pass

    def test_005_enter_valid_data_in_old_password_new_password___tap_on_submit_button(self):
        """
        DESCRIPTION: Enter valid data in 'Old Password', 'New Password' -> tap on 'Submit' button
        EXPECTED: Password changed successfully! message appears
        EXPECTED: ![](index.php?/attachments/get/14054200)
        """
        pass

    def test_006_log_out_and_try_to_log_in_with_old_password(self):
        """
        DESCRIPTION: Log out and try to log in with old password
        EXPECTED: It is impossible to login with old password
        """
        pass

    def test_007_log_in_with_new_password(self):
        """
        DESCRIPTION: Log in with new password
        EXPECTED: User is logged in
        """
        pass
