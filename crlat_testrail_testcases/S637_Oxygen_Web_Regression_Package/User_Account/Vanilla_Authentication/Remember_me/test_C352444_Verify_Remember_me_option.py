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
class Test_C352444_Verify_Remember_me_option(Common):
    """
    TR_ID: C352444
    NAME: Verify 'Remember me' option
    DESCRIPTION: This test case verifies 'Remember me' option on Log in pop-up
    PRECONDITIONS: 1. User should have 'Not defined' session limits (My Account > Settings > Gambling Controls > Time Management)
    PRECONDITIONS: 2. Load Oxygen app. Homepage is opened
    """
    keep_browser_open = True

    def test_001_tap_on_log_in_button(self):
        """
        DESCRIPTION: Tap on "Log In" button
        EXPECTED: * 'Log in' pop-up is opened
        EXPECTED: * 'Remember me' checkbox is located under 'Password' field and is unchecked by default
        """
        pass

    def test_002_check_out_remember_me_checkbox(self):
        """
        DESCRIPTION: Check out "Remember Me" checkbox
        EXPECTED: Checkbox is highlighted with a "tick"
        """
        pass

    def test_003_fill_in_log_in_form_with_valid_credentials_and_tap_on_log_in_button(self):
        """
        DESCRIPTION: Fill in "Log In" form with valid credentials and tap on "Log In" button
        EXPECTED: User is successfully logged in with permanent session
        """
        pass

    def test_004_log_out_from_the_app(self):
        """
        DESCRIPTION: Log out from the app
        EXPECTED: User is logged out
        """
        pass

    def test_005_close_browser_window(self):
        """
        DESCRIPTION: Close browser window
        EXPECTED: 
        """
        pass

    def test_006_open_browser_load_oxygen_app_and_tap_on_log_in_button(self):
        """
        DESCRIPTION: Open browser, load Oxygen app and tap on "Log In" button
        EXPECTED: * 'Log in' pop-up is opened
        EXPECTED: * 'Remember me' checkbox is checked
        """
        pass

    def test_007_uncheck_remember_me_checkbox_enter_valid_credentials_and_tap_log_in_button(self):
        """
        DESCRIPTION: Uncheck 'Remember me' checkbox, enter valid credentials and tap 'Log in' button
        EXPECTED: User is logged in without permanent session
        """
        pass

    def test_008_log_out_from_the_app(self):
        """
        DESCRIPTION: Log out from the app
        EXPECTED: 
        """
        pass

    def test_009_tap_on_log_in_button(self):
        """
        DESCRIPTION: Tap on "Log In" button
        EXPECTED: * 'Log in' pop-up is opened
        EXPECTED: * 'Remember me' checkbox is unchecked
        """
        pass
