import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C518423_Verify_Log_In_Bet_for_the_User_with_Positive_Balance(Common):
    """
    TR_ID: C518423
    NAME: Verify 'Log In & Bet' for the User with Positive Balance
    DESCRIPTION: This test case verifies 'Log In & Bet' button for a logged out and logged in user
    PRECONDITIONS: Make sure you have user account with added credit cards and positive balance
    """
    keep_browser_open = True

    def test_001_add_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add selection(s) to the Betslip
        EXPECTED: 
        """
        pass

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: 1. Betslip is opened
        EXPECTED: 2. Added selection(s) present on the Betslip
        EXPECTED: 3. 'Log in & Bet' button is disabled
        EXPECTED: **From OX99**
        EXPECTED: Button name:
        EXPECTED: Coral: 'Login & Place Bet'
        EXPECTED: Ladbrokes: 'Login and Place bet
        """
        pass

    def test_003_enter_at_least_one_stake_for_any_selection(self):
        """
        DESCRIPTION: Enter at least one stake for any selection
        EXPECTED: 'Log in & Bet' button becomes enabled
        """
        pass

    def test_004_tap_on_log_in__bet_button(self):
        """
        DESCRIPTION: Tap on 'Log in & Bet' button
        EXPECTED: 'Log In' pop-up is opened
        """
        pass

    def test_005_log_in_with_user_that_has_added_credit_cards_and_positive_balance(self):
        """
        DESCRIPTION: Log in with user that has **added credit cards and positive balance**
        EXPECTED: 1. Betslip is refreshed
        EXPECTED: 2. User is logged in
        EXPECTED: 3. Bet is placed automatically
        EXPECTED: (NOTE: if at least one pop-up is expected after login, Bet is NOT placed automatically)
        EXPECTED: 4. Bet Receipt is shown
        """
        pass
