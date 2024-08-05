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
class Test_C1107967_Verify_registration_through_Gaming_Homepage_after_logging_in_out_with_gaming_sports_transitions(Common):
    """
    TR_ID: C1107967
    NAME: Verify registration through Gaming Homepage, after logging in/out with gaming <> sports transitions
    DESCRIPTION: Verify registration through Gaming Homepage, after logging in/out with gaming <> sports transitions
    PRECONDITIONS: **Choosing the password should include following rules:**
    PRECONDITIONS: * At least 8 characters;
    PRECONDITIONS: * Uppercase and lowercase letters;
    PRECONDITIONS: * Numbers and symbols
    """
    keep_browser_open = True

    def test_001_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: Oxygen page is loaded
        """
        pass

    def test_002_clicktap_on_gaming_tab(self):
        """
        DESCRIPTION: Click/Tap on Gaming tab
        EXPECTED: 'Gaming' homepage is loaded
        """
        pass

    def test_003_clicktap_on_log_in_button_and_fill_valid_credentials(self):
        """
        DESCRIPTION: Click/Tap on 'LOG IN' button and fill valid credentials
        EXPECTED: User is logged in
        """
        pass

    def test_004_clicktap_on_sports(self):
        """
        DESCRIPTION: Click/Tap on Sports
        EXPECTED: Oxygen page is loaded
        """
        pass

    def test_005_clicktap_on_gaming_tab(self):
        """
        DESCRIPTION: Click/Tap on Gaming tab
        EXPECTED: 'Gaming' homepage is loaded
        """
        pass

    def test_006_clicktap_on_balance_account_and_log_out(self):
        """
        DESCRIPTION: Click/Tap on 'Balance Account' and log out
        EXPECTED: User is logged out
        """
        pass

    def test_007_clicktap_on_join_now_button(self):
        """
        DESCRIPTION: Click/Tap on 'JOIN NOW' button
        EXPECTED: Following pages are loaded:
        EXPECTED: * Page 'Registration - Step 1 of 2' is shown on Desktop/ Tablet
        EXPECTED: * Page 'Registration - Step 1 of 3' is shown on Mobile devices
        """
        pass

    def test_008_go_to_oxygen_homepage_and_repeat_steps_3_7_but_on_step_3_log_in_with_remember_option_set(self):
        """
        DESCRIPTION: Go to Oxygen Homepage and repeat steps #3-7, but on step #3 log in with 'Remember' option set
        EXPECTED: 
        """
        pass
