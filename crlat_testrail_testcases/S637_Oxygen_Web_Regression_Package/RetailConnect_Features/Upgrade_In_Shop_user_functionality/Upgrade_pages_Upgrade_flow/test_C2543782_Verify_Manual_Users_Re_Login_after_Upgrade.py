import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2543782_Verify_Manual_Users_Re_Login_after_Upgrade(Common):
    """
    TR_ID: C2543782
    NAME: Verify Manual User's Re-Login after Upgrade
    DESCRIPTION: This test case verifies manual re-login flow after in-shop user upgrade
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in with in-shop user
    """
    keep_browser_open = True

    def test_001_tap_upgrade_button_on_the_upgrade_popup(self):
        """
        DESCRIPTION: Tap **UPGRADE** button on the Upgrade popup
        EXPECTED: A user is redirected to the 'registration' screen
        """
        pass

    def test_002_provide_all_necessary_data_and_upgrade_your_account(self):
        """
        DESCRIPTION: Provide all necessary data and upgrade your account
        EXPECTED: User is logged out from the app and redirected to the login page with a message 'You have upgraded your account. Please use your Username and Password to log in with."
        """
        pass

    def test_003_log_in_with_username_and_password_entered_during_upgrade(self):
        """
        DESCRIPTION: Log in with username and password entered during upgrade
        EXPECTED: User is successfully logged in
        """
        pass
