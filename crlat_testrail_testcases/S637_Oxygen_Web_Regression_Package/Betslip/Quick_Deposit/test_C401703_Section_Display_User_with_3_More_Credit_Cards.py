import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C401703_Section_Display_User_with_3_More_Credit_Cards(Common):
    """
    TR_ID: C401703
    NAME: Section Display User with 3/ More Credit Cards
    DESCRIPTION: This test case verifies Payment methods display within Quick Deposit Section on Betslip area in case User  has 4 or more Credit Cards registered.
    DESCRIPTION: ** JIRA tickets:**
    DESCRIPTION: BMA-20368 Betslip design - Quick deposit section
    DESCRIPTION: BMA-20463 New betslip - Nummeric keyboard (mobile only)
    PRECONDITIONS: User account with balance <20 and more than one Credit Cards
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: - Homepage is shown
        """
        pass

    def test_002_login_with_user_account_from_preconditions(self):
        """
        DESCRIPTION: Login with user account (from preconditions)
        EXPECTED: - User is logged in
        """
        pass

    def test_003_add_a_selection_to_the_betslip_and_open_bet_slip_page___widget(self):
        """
        DESCRIPTION: Add a selection to the Betslip and open Bet Slip page  / widget
        EXPECTED: - Selection is displayed within Betslip content area
        EXPECTED: - Numeric keyboard with 'Quick stakes' buttons are displayed (mobile only)
        """
        pass

    def test_004_enter_stake_that_is_greater_than_users_balance(self):
        """
        DESCRIPTION: Enter Stake that is greater than User's Balance
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        pass

    def test_005_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: - All credit cards are displayed within Quick Deposit Section  and based on device resolution are displayed  in few rows  by 3-X and marked with green tick icon
        EXPECTED: - The 'Deposit Amount' field is auto-populated with the calculated funds needed to cover the User’s bet
        """
        pass
