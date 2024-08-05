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
class Test_C34589253_Verify_User_Session_when_Remember_me_option_is_set(Common):
    """
    TR_ID: C34589253
    NAME: Verify User Session when 'Remember me' option is set
    DESCRIPTION: This test case verifies User Session when 'Remember me' option is set
    PRECONDITIONS: User should have 'Not Defined' session limits
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_clicktap_log_in_button(self):
        """
        DESCRIPTION: Click/Tap 'Log in' button
        EXPECTED: 'Log in' pop-up is present
        """
        pass

    def test_003_enter_valid_credentials_check_remember_me_checkbox_and_tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials, check 'Remember me' checkbox and tap 'Log in' button
        EXPECTED: User is logged in with permanent session
        """
        pass

    def test_004_navigate_through_the_application(self):
        """
        DESCRIPTION: Navigate through the application
        EXPECTED: User stays logged in
        """
        pass

    def test_005_refresh_app_via_refresh_button(self):
        """
        DESCRIPTION: Refresh app via refresh button
        EXPECTED: User stays logged in
        """
        pass

    def test_006_go_to_gaming_lobby_and_back_to_oxygen(self):
        """
        DESCRIPTION: Go to Gaming lobby and back to Oxygen
        EXPECTED: User stays logged in
        """
        pass

    def test_007_for_mobiletabletlock_device(self):
        """
        DESCRIPTION: **For Mobile/Tablet**
        DESCRIPTION: Lock device
        EXPECTED: 
        """
        pass

    def test_008_for_mobiletabletunlock_device___open_app(self):
        """
        DESCRIPTION: **For Mobile/Tablet**
        DESCRIPTION: Unlock device -> open app
        EXPECTED: **For Mobile/Tablet**
        EXPECTED: User stays logged in
        """
        pass

    def test_009_killclose_browser(self):
        """
        DESCRIPTION: Kill/Close browser
        EXPECTED: 
        """
        pass

    def test_010_load_browser_and_app(self):
        """
        DESCRIPTION: Load browser and app
        EXPECTED: User stays logged in
        """
        pass

    def test_011_for_mobiletabletput_app_in_background_and_wait_for_some_time(self):
        """
        DESCRIPTION: **For Mobile/Tablet**
        DESCRIPTION: Put app in background and wait for some time
        EXPECTED: 
        """
        pass

    def test_012_for_mobiletabletgo_back_to_app(self):
        """
        DESCRIPTION: **For Mobile/Tablet**
        DESCRIPTION: Go back to app
        EXPECTED: * User stays logged in
        """
        pass
