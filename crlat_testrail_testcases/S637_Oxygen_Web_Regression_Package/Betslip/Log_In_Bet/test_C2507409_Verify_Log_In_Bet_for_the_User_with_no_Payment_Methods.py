import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2507409_Verify_Log_In_Bet_for_the_User_with_no_Payment_Methods(Common):
    """
    TR_ID: C2507409
    NAME: Verify 'Log In & Bet' for the User with no Payment Methods
    DESCRIPTION: This test case verifies 'Log In & Bet' button for a logged out and logged in user
    PRECONDITIONS: Make sure you have user account with:
    PRECONDITIONS: No payment methods with 0/or insufficient balance
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
        EXPECTED: 2. Added single selection(s) present
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

    def test_005_log_in_with_user_that_has_no_payment_methods(self):
        """
        DESCRIPTION: Log in with user that has **no payment methods**
        EXPECTED: 1. 'Please deposit a min of xx.xx to continue placing your bet' pop-up appears
        EXPECTED: 2. Bet is NOT placed
        """
        pass

    def test_006_click_make_a_deposit_button(self):
        """
        DESCRIPTION: Click 'Make a deposit' button
        EXPECTED: 1. User is navigated to 'Deposit' page, 'Add Credit/Debit Cards' tab for **Coral** brand
        EXPECTED: 2. User is navigated to Account One system for **Ladbrokes** brand
        EXPECTED: 3. Bet is NOT placed
        """
        pass
