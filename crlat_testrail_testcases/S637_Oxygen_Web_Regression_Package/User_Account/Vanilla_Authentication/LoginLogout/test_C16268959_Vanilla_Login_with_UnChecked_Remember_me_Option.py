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
class Test_C16268959_Vanilla_Login_with_UnChecked_Remember_me_Option(Common):
    """
    TR_ID: C16268959
    NAME: [Vanilla] Login with UnChecked "Remember me" Option
    DESCRIPTION: This Test Case verify that if "Remember" me Option is UnChecked, then User should be logged out after User session expiration: On Beta it 2h;
    PRECONDITIONS: User should not be logged in
    """
    keep_browser_open = True

    def test_001_clicktap_on_the_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on the "Log In" button
        EXPECTED: *   "Log In" pop-up is opened
        EXPECTED: *   Username and Password fields are available
        EXPECTED: *   "Remember me" checkbox is placed under Username field and unchecked by default
        """
        pass

    def test_002_enter_valid_login_and_password_and_do_not_check_remember_me_option(self):
        """
        DESCRIPTION: Enter valid Login and Password and DO NOT check 'Remember me' option
        EXPECTED: User is successfully logged in
        """
        pass

    def test_003_take_the_application_to_the_background_for__2_h_and_wait_until_session_will_be_expired(self):
        """
        DESCRIPTION: Take the application to the background for  2 h and wait until session will be expired;
        EXPECTED: 2 h was passed;
        """
        pass

    def test_004_open_app_again_and_wait_until_it_loads(self):
        """
        DESCRIPTION: Open App again and wait until it loads;
        EXPECTED: - App is loaded and previously logged in User is logged out;
        """
        pass
