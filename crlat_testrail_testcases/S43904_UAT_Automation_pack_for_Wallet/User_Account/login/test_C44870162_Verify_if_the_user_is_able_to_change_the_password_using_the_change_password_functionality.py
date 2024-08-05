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
class Test_C44870162_Verify_if_the_user_is_able_to_change_the_password_using_the_change_password_functionality(Common):
    """
    TR_ID: C44870162
    NAME: Verify if the user is able to change the password using the 'change password'  functionality
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: Load https://beta-sports.coral.co.uk/
        EXPECTED: 
        """
        pass

    def test_002_log_in_with_valid_credentials(self):
        """
        DESCRIPTION: Log in with valid credentials
        EXPECTED: User is successfully logged in
        EXPECTED: Home page is opened in case if user has positive amount of his/her balance
        EXPECTED: Low Balance message is shown to the user if balance is equal to 0 (Not Applicable for Ladbrokes)
        """
        pass

    def test_003_click_on_the_avatar__settings__change_password(self):
        """
        DESCRIPTION: Click on the Avatar > Settings > Change password
        EXPECTED: 'Change Password' page is opened
        """
        pass

    def test_004_enter_valid_data_in_old_password_new_password_and_tapclick_on_submit_button(self):
        """
        DESCRIPTION: Enter valid data in 'Old Password', 'New Password' and tap/click on 'Submit' button
        EXPECTED: Confirmation message appears under the header ("Password changed successfully!!")
        EXPECTED: Password is changed
        EXPECTED: User is still logged in
        """
        pass

    def test_005_log_out_and_login_again_with_new_password(self):
        """
        DESCRIPTION: Log out and login again with new password
        EXPECTED: User is logged in with new password
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
