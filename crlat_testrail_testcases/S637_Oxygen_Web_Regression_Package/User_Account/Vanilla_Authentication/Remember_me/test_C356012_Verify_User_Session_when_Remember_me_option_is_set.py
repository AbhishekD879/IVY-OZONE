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
class Test_C356012_Verify_User_Session_when_Remember_me_option_is_set(Common):
    """
    TR_ID: C356012
    NAME: Verify User Session when 'Remember me' option is set
    DESCRIPTION: This test case verifies User Session when 'Remember me' option is set
    PRECONDITIONS: 1. User should have 'Not defined' session limits (My Account > Settings > Gambling Controls > Time Management)
    PRECONDITIONS: 2. Load Oxygen app. Homepage is opened
    """
    keep_browser_open = True

    def test_001_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log in' button
        EXPECTED: 'Log in' pop-up is present
        """
        pass

    def test_002_enter_valid_credentials_check_remember_me_checkbox_and_tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials, check 'Remember me' checkbox and tap 'Log in' button
        EXPECTED: User is logged in with permanent session
        """
        pass

    def test_003_navigate_through_the_application(self):
        """
        DESCRIPTION: Navigate through the application
        EXPECTED: User stays logged in
        """
        pass

    def test_004_refresh_app_via_refresh_button(self):
        """
        DESCRIPTION: Refresh app via refresh button
        EXPECTED: User stays logged in
        """
        pass

    def test_005_go_to_gaming_lobby_and_back_to_oxygen(self):
        """
        DESCRIPTION: Go to Gaming lobby and back to Oxygen
        EXPECTED: User stays logged in
        """
        pass

    def test_006_lock_device(self):
        """
        DESCRIPTION: Lock device
        EXPECTED: 
        """
        pass

    def test_007_unlock_device___open_app(self):
        """
        DESCRIPTION: Unlock device -> open app
        EXPECTED: User stays logged in
        """
        pass

    def test_008_kill_browser(self):
        """
        DESCRIPTION: Kill browser
        EXPECTED: 
        """
        pass

    def test_009_load_browser_and_app(self):
        """
        DESCRIPTION: Load browser and app
        EXPECTED: User stays logged in
        """
        pass

    def test_010_put_app_in_background_and_wait_for_a_few_hoursdays(self):
        """
        DESCRIPTION: Put app in background and wait for a few hours/days
        EXPECTED: 
        """
        pass

    def test_011_go_back_to_app(self):
        """
        DESCRIPTION: Go back to app
        EXPECTED: * User stays logged in
        EXPECTED: * Session timer is displayed at the bottom of page
        """
        pass
