import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C18228257_Verify_Quick_Bet_after_logout(Common):
    """
    TR_ID: C18228257
    NAME: Verify Quick Bet after logout
    DESCRIPTION: This test case verifies Quick Bet after logout
    DESCRIPTION: AUTOTEST [C9697669]
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user's settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. In order to trigger case when the session is over, perform the next steps:
    PRECONDITIONS: * Log in to one browser tab
    PRECONDITIONS: * Duplicate tab
    PRECONDITIONS: * Log out from the second tab -> session is over in both tabs
    PRECONDITIONS: 4. Application is loaded
    PRECONDITIONS: 5. User is logged in
    """
    keep_browser_open = True

    def test_001_add_sportrace_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add <Sport>/<Race> selection to Quick Bet
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        EXPECTED: * Added selection and all data are displayed in Quick Bet
        """
        pass

    def test_002_enter_value_in_stake_field_and_select_ew_checkbox_if_available(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and select 'E/W' checkbox (if available)
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'E/W' checkbox is selected
        """
        pass

    def test_003_make_steps_listed_in_preconditions(self):
        """
        DESCRIPTION: Make steps listed in preconditions
        EXPECTED: User session is over
        """
        pass

    def test_004_verify_quick_betneed_to_be_updated_for_coral_vanilla(self):
        """
        DESCRIPTION: Verify Quick Bet
        DESCRIPTION: (**NEED TO BE UPDATED FOR CORAL-VANILLA**)
        EXPECTED: * 'Log out' pop-up is
        EXPECTED: * Quick Bet stays
        EXPECTED: * 'BET NOW' button becomes 'LOG IN & BET
        EXPECTED: * Entered on step #4 value is
        EXPECTED: * 'E/W' checkbox stays selected
        """
        pass

    def test_005_tap_x_button_on_log_out_pop_up(self):
        """
        DESCRIPTION: Tap 'X' button on 'Log out' pop-up
        EXPECTED: * 'Log out' pop-up is closed
        EXPECTED: * Quick Bet stays opened
        """
        pass
