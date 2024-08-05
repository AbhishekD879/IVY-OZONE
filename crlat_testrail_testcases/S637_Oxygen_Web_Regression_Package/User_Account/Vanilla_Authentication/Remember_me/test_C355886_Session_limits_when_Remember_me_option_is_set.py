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
class Test_C355886_Session_limits_when_Remember_me_option_is_set(Common):
    """
    TR_ID: C355886
    NAME: Session limits when 'Remember me' option is set
    DESCRIPTION: This test case verifies session limits when 'Remember me' option is set
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_tap_log_in_button(self):
        """
        DESCRIPTION: Load Oxygen app, tap 'Log in' button
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_002_enter_valid_credentials_check_remember_me_option_and_tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials, check 'Remember me' option and tap 'Log in' button
        EXPECTED: User is logged in successfully with permanent session
        """
        pass

    def test_003_go_to_my_account__settings__gambling_controls__time_management(self):
        """
        DESCRIPTION: Go to My Account > Settings > Gambling Controls > Time Management
        EXPECTED: * "Time Management" view opens.
        EXPECTED: * "No time limit" should be selected by default.
        """
        pass

    def test_004_select_one_of_the_options_eg_15_minutes_and_click_on_the_button_save(self):
        """
        DESCRIPTION: Select one of the options (e.g. 15 minutes) and click on the button "Save"
        EXPECTED: Success message appears under the "Time management" header: "Your time management settings have been successfully saved."
        """
        pass

    def test_005_wait_until_session_limit_will_be_reached(self):
        """
        DESCRIPTION: Wait until session limit will be reached
        EXPECTED: * User is logged out automatically, no matter that he has permanent session
        """
        pass

    def test_006_repeat_steps_1_5_but_on_step_4_choose_other_limit(self):
        """
        DESCRIPTION: Repeat steps #1-5, but on step 4 choose other limit
        EXPECTED: 
        """
        pass
