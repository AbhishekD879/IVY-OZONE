import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C16268989_Vanilla_Verify_login_from_same_device_ip_browser(Common):
    """
    TR_ID: C16268989
    NAME: [Vanilla] Verify login from same device/ip/browser
    DESCRIPTION: This test case verifies login from the same browsers/same IP but using new browser instance.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_login_to_oxygen(self):
        """
        DESCRIPTION: Login to Oxygen
        EXPECTED: Right menu button is shown
        """
        pass

    def test_002_open_oxygen_application_in_a_new_bowser_instance(self):
        """
        DESCRIPTION: Open Oxygen application in a new bowser instance
        EXPECTED: Home page is loaded
        """
        pass

    def test_003_in_browser_opened_in_step_2_login_with_the_same_account_as_in_step1(self):
        """
        DESCRIPTION: In browser opened in step 2 login with the same account as in step1
        EXPECTED: Right menu button is shown
        """
        pass

    def test_004_from_right_menu_select_logout_option(self):
        """
        DESCRIPTION: From Right menu select logout option
        EXPECTED: 'Join us' button is visible on header
        """
        pass

    def test_005_close_the_2nd_browser(self):
        """
        DESCRIPTION: Close the 2nd browser
        EXPECTED: The first browser instance is active
        """
        pass

    def test_006_check_the_app_view_in_first_browser(self):
        """
        DESCRIPTION: Check the App view in first browser
        EXPECTED: User stays logged in
        """
        pass
