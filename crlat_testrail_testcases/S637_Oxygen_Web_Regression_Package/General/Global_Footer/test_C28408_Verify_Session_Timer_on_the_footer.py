import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C28408_Verify_Session_Timer_on_the_footer(Common):
    """
    TR_ID: C28408
    NAME: Verify Session Timer on the footer
    DESCRIPTION: ONLY FOR CORAL. For Ladbrokes, this shouldn't be shown.
    DESCRIPTION: This test case verifies Session Timer on the Global Footer
    PRECONDITIONS: User is logged out
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_verify_session_timer_presence_on_the_global_footer(self):
        """
        DESCRIPTION: Verify Session Timer presence on the Global Footer
        EXPECTED: Session Timer is absent
        """
        pass

    def test_003_log_in_to_oxygen_application_without_remember_me_option_set(self):
        """
        DESCRIPTION: Log in to Oxygen application without 'Remember me' option set
        EXPECTED: User is logged in
        """
        pass

    def test_004_verify_session_timer_presence_on_the_global_footercoral_only(self):
        """
        DESCRIPTION: Verify Session Timer presence on the Global Footer
        DESCRIPTION: (Coral Only)
        EXPECTED: *   Session Timer is present with inscription: 'You have been logged in:  MM:SS'
        EXPECTED: *   Session Timer is counting according to session time for the current user
        """
        pass

    def test_005_verify_session_timer_format(self):
        """
        DESCRIPTION: Verify Session Timer format
        EXPECTED: *   Initial format is **MM:SS**
        EXPECTED: *   Session Timer is shown in the **HH:MM:SS** format after 59:59
        EXPECTED: * Session Timer is shown in the **DD day HH:MM:SS** format after 23:59:59
        """
        pass

    def test_006_turn_phone_to_the_sleep_mode_and_check_session_timer_after_few_minuteshoursdays(self):
        """
        DESCRIPTION: Turn phone to the sleep mode and check Session Timer after few minutes/hours/days
        EXPECTED: Session Timer is reflected according to session time for the current session
        """
        pass

    def test_007_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED: Session Timer is no more shown on the Global Footer
        """
        pass

    def test_008_log_in_oxygen_application_with_remember_me_option_set_and_repeat_step_4_5(self):
        """
        DESCRIPTION: Log in Oxygen application with 'Remember me' option set and repeat step #4-5
        EXPECTED: 
        """
        pass

    def test_009_turn_phone_to_the_sleep_mode_and_check_session_timer_after_few_minuteshoursdaysnote_that_in_this_case_new_ws_connection_should_be_created_and_user_must_be_re_logged_in_into_oxygen_app(self):
        """
        DESCRIPTION: Turn phone to the sleep mode and check Session Timer after few minutes/hours/days
        DESCRIPTION: **NOTE** that in this case new WS connection should be created and user must be re-logged in into Oxygen app
        EXPECTED: Session timer is reset to 0:00
        """
        pass

    def test_010_only_for_ladbrokes(self):
        """
        DESCRIPTION: ONLY FOR LADBROKES.
        EXPECTED: For Ladbrokes, the Timer shouldn't be shown.
        """
        pass
