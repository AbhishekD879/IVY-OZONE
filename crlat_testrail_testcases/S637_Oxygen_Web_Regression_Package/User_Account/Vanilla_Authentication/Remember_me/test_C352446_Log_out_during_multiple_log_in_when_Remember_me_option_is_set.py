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
class Test_C352446_Log_out_during_multiple_log_in_when_Remember_me_option_is_set(Common):
    """
    TR_ID: C352446
    NAME: Log out during multiple log in when 'Remember me' option is set
    DESCRIPTION: This test case verifies log out during multiple log in when 'Remember me' option is set
    DESCRIPTION: AUTOTEST [C9697725]
    PRECONDITIONS: 1. User should have 'Not defined' session limits (My Account > Settings > Gambling Controls > Time Management)
    PRECONDITIONS: 2. Load Oxygen app. Homepage is opened
    """
    keep_browser_open = True

    def test_001_log_in_from_device_1_with_remember_me_option_set(self):
        """
        DESCRIPTION: Log in from Device 1 with 'Remember me' option set
        EXPECTED: User is logged in successfully with permanent session
        """
        pass

    def test_002_load_oxygen_app_and_log_in_with_the_same_credentials_on_device_2(self):
        """
        DESCRIPTION: Load Oxygen app and log in with the same credentials on Device 2
        EXPECTED: User is logged in successfully without permanent session
        """
        pass

    def test_003_log_out_from_device_2(self):
        """
        DESCRIPTION: Log out from Device 2
        EXPECTED: User is logged out
        """
        pass

    def test_004_navigate_through_device_1(self):
        """
        DESCRIPTION: Navigate through Device 1
        EXPECTED: * User stays logged in
        EXPECTED: * Session is NOT expired on Device 1
        """
        pass

    def test_005_repeat_steps_1_4_but_on_step_1_put_app_in_background_and_wait_for_a_few_minutes_or_close_browsernavigate_to_another_app_eg_google(self):
        """
        DESCRIPTION: Repeat steps #1-4 but on step 1 put app in background and wait for a few minutes or close browser/navigate to another app (e.g. google)
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_1_5_but_on_step_2_log_in_with_remember_me_option_set(self):
        """
        DESCRIPTION: Repeat steps #1-5 but on step 2 log in with 'Remember me' option set
        EXPECTED: 
        """
        pass
