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
class Test_C62799662_Verify_Place_Bet_and_Stake_fields_are_in_disable_state_during_self_exclusion_in_Betslip(Common):
    """
    TR_ID: C62799662
    NAME: Verify Place Bet and Stake fields are in disable state during self-exclusion in Betslip
    DESCRIPTION: This test case verifies disable  of place bet and stake field
    PRECONDITIONS: User should be logged in to view 'Self Exclusion' message and buttons
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_selection_to_betslip(self):
        """
        DESCRIPTION: Add selection to betslip
        EXPECTED: Added selection and all data are displayed in betslip
        """
        pass

    def test_003_enter_at_least_one_stake_for_any_selection(self):
        """
        DESCRIPTION: Enter at least one stake for any selection
        EXPECTED: 'Login & Place Bet' button becomes enabled
        """
        pass

    def test_004_tap_login__place_bet_button(self):
        """
        DESCRIPTION: Tap 'Login & Place Bet' button
        EXPECTED: Log In' pop-up opens
        EXPECTED: Username and Password fields are available
        """
        pass

    def test_005_enter_valid_credentials_of_users_account_which_is_self_excluded(self):
        """
        DESCRIPTION: Enter valid credentials of user's account which is Self-excluded
        EXPECTED: User should be logged in and clear the stake amount on place bet and stake textbox disable, User will see a message on Betslip
        """
        pass
