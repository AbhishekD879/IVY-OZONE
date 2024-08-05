import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C28237_Homepage_Tutorial_Overlay_displaying_after_new_Terms_and_Conditions_accepting_declining(Common):
    """
    TR_ID: C28237
    NAME: Homepage Tutorial Overlay displaying after new Terms and Conditions accepting/declining
    DESCRIPTION: This test case verifies Homepage Tutorial Overlay displaying after new Terms and Conditions accepting/declining
    PRECONDITIONS: JIRA tickets:
    PRECONDITIONS: BMA-7029 Homepage Tutorial Overlay
    PRECONDITIONS: Information that Homepage Tutorial Overlay was shown is saved in Local Storage: name - OX.tutorial, value - True. Cookie is added after Overlay closing via 'Close' or My Bets/Betslip/Balance buttons
    PRECONDITIONS: *   Terms and Conditions have been changed
    PRECONDITIONS: *   In order to trigger T&C change additional setup should be made by UAT team
    PRECONDITIONS: ![](index.php?/attachments/get/1228)
    """
    keep_browser_open = True

    def test_001_clear_browser_cookies_and_load_invictus_application(self):
        """
        DESCRIPTION: Clear browser cookies and load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_on_log_in_pop_up_dialog_fill_in_all_fields_with_valid_datatap_log_in_button(self):
        """
        DESCRIPTION: On log in pop-up dialog fill in all fields with valid data.
        DESCRIPTION: Tap 'Log in' button.
        EXPECTED: 'Terms and Conditions' dialog is displayed with a message asking the user to acept new Terms ad Conditions
        """
        pass

    def test_003_tap_ok_button_to_accept_new_tc(self):
        """
        DESCRIPTION: Tap 'Ok' button to accept new T&C
        EXPECTED: *   Terms and Conditions are accepted
        EXPECTED: *   User is logged in
        EXPECTED: *   Homepage is displayed
        EXPECTED: *   Homepage Tutorial Overlay is displayed
        """
        pass

    def test_004_repeat_steps_1_and_2do_not_accept_new_tc_and_close_appropriate_pop_up_dialog(self):
        """
        DESCRIPTION: Repeat steps 1 and 2.
        DESCRIPTION: Do NOT accept new T&C and close appropriate pop-up dialog
        EXPECTED: *   Homepage is displayed
        EXPECTED: *   User is not logged in to application
        EXPECTED: *   Homepage Tutorial Overlay is NOT displayed
        """
        pass
