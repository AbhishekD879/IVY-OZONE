import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.user_account
@vtest
class Test_C17699659_Vanilla_Verify_manual_trigger_of_Vanilla_login_flow_after_app_restart_with_Remember_me_option(Common):
    """
    TR_ID: C17699659
    NAME: [Vanilla] Verify manual trigger of Vanilla login flow after app restart with "Remember me" option
    DESCRIPTION: This test case verifies how Vanilla login flow is triggered after application is being restarted
    PRECONDITIONS: The app is installed and launched.
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is loaded successfully
        """
        self.site.wait_content_state('Homepage')

    def test_002_tap_on_log_in_button(self):
        """
        DESCRIPTION: Tap on 'Log In' button
        EXPECTED: 'Log in' form is opened
        """
        self.site.login(remember_me=True)

    def test_003___enter_valid_credentials__tap_on_log_in_button(self):
        """
        DESCRIPTION: - Enter valid credentials
        DESCRIPTION: - Tap on 'Log In' button
        EXPECTED: User is logged in successfully.
        """
        # covered in step 2

    def test_004_navigate_through_the_application(self):
        """
        DESCRIPTION: Navigate through the application
        EXPECTED: User stays logged in
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_005_kill_the_application_on_the_device(self):
        """
        DESCRIPTION: Kill the application on the device
        EXPECTED: Application is closed
        """
        self.device.open_new_tab()
        self.device.open_tab(tab_index=0)
        self.device.close_current_tab()
        self.device.switch_to_new_tab()

    def test_006_launch_app_again(self):
        """
        DESCRIPTION: Launch app again
        EXPECTED: - App is opened
        EXPECTED: - User is logged in
        """
        self.device.navigate_to(tests.HOSTNAME)
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')

    def test_007_navigate_through_the_application(self):
        """
        DESCRIPTION: Navigate through the application
        EXPECTED: User stays logged in
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')
