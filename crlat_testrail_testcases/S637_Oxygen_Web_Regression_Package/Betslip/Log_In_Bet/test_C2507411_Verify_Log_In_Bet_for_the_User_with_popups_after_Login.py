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
class Test_C2507411_Verify_Log_In_Bet_for_the_User_with_popups_after_Login(Common):
    """
    TR_ID: C2507411
    NAME: Verify 'Log In & Bet' for the User with popups after Login
    DESCRIPTION: This test case verifies 'Log In & Bet' button for a logged out and logged in user
    DESCRIPTION: AUTOTEST: [C2604438]
    PRECONDITIONS: Make sure you have user account with added credit cards with positive balance, however for this user popups are expected after login (e.g., Freebet popup, NetVerify, Bonuses, etc.)
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

    def test_005_log_in_with_user_that_has_added_credit_cards_with_positive_balance_and_pop_ups_are_expected_after_login(self):
        """
        DESCRIPTION: Log in with user that has **added credit cards with positive balance** and pop-ups are expected after login
        EXPECTED: 1. User is logged in
        EXPECTED: 2. Expected popup is shown
        """
        pass

    def test_006_close_popup(self):
        """
        DESCRIPTION: Close popup
        EXPECTED: 1. Popup is closed
        EXPECTED: 2. Bet is NOT placed automatically
        EXPECTED: 3. Button states 'Bet Now'
        EXPECTED: 4. 'Bet Now' button is enabled
        EXPECTED: **From OX99**
        EXPECTED: Button name:
        EXPECTED: Coral and Ladbrokes: 'Place Bet'
        """
        pass
