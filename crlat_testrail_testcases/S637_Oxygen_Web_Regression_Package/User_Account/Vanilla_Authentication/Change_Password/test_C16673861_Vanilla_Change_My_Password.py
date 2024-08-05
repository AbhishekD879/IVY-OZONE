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
class Test_C16673861_Vanilla_Change_My_Password(Common):
    """
    TR_ID: C16673861
    NAME: [Vanilla] Change My Password
    DESCRIPTION: This test case verifies 'Change Password' functionality
    PRECONDITIONS: Choosing the password should include following rules:
    PRECONDITIONS: * At least 8 characters;
    PRECONDITIONS: * Uppercase and lowercase letters;
    PRECONDITIONS: * Numbers and symbols
    """
    keep_browser_open = True

    def test_001_load_home_page(self):
        """
        DESCRIPTION: Load Home page
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_with_valid_credentials(self):
        """
        DESCRIPTION: Log in with valid credentials
        EXPECTED: User is logged in successfully
        """
        pass

    def test_003_clicktap_on_my_account_menu_on_the_upper_right_side_of_the_pageindexphpattachmentsget34267(self):
        """
        DESCRIPTION: Click/Tap on "My Account" Menu on the upper right side of the page
        DESCRIPTION: ![](index.php?/attachments/get/34267)
        EXPECTED: "My Account" menu is displayed
        EXPECTED: ![](index.php?/attachments/get/34268)
        """
        pass

    def test_004_clicktap_on_settings____change_password_menu_on_the_item(self):
        """
        DESCRIPTION: Click/Tap on **'Settings'** --> "**'Change Password'**" menu on the item
        EXPECTED: "**'Change Password'**" page is opened
        """
        pass

    def test_005_verify_change_passwordpage(self):
        """
        DESCRIPTION: Verify 'Change Password' page
        EXPECTED: 'Change password' page consists of the following:
        EXPECTED: 1.  Page title is **'CHANGE PASSWORD'**
        EXPECTED: 2.  Back button near title (left side)
        EXPECTED: 3.  Close button in the upper right corner
        EXPECTED: 4.  **'Old Password', 'New Password' fields
        EXPECTED: 5.  Show Password icon for each field
        EXPECTED: 4.  **'SUBMIT'** button, enabled by default
        EXPECTED: ![](index.php?/attachments/get/34269)
        """
        pass

    def test_006_verify_backbutton(self):
        """
        DESCRIPTION: Verify Back button
        EXPECTED: User gets back to previous page ("Settings" page )
        """
        pass

    def test_007_click_on_change_password_againenter_valid_data_in_old_password_new_password___tap_on_submit_button(self):
        """
        DESCRIPTION: Click on 'Change Password' again
        DESCRIPTION: Enter valid data in 'Old Password', 'New Password' -> tap on 'Submit' button
        EXPECTED: 1.  Field validation message should appear while entering NewPassword
        EXPECTED: ![](index.php?/attachments/get/34270)
        EXPECTED: 2.  Password changed successfully! message appears
        EXPECTED: ![](index.php?/attachments/get/34271)
        EXPECTED: 3.  'Change Password' form remains opened
        EXPECTED: 4.  All fields are cleared
        """
        pass

    def test_008_log_out___try_to_log_in_with_old_password(self):
        """
        DESCRIPTION: Log out -> try to log in with old password
        EXPECTED: It is impossible to login with old password
        """
        pass

    def test_009_log_in_with_new_password(self):
        """
        DESCRIPTION: Log in with new password
        EXPECTED: User is logged in successfully with new password
        """
        pass
