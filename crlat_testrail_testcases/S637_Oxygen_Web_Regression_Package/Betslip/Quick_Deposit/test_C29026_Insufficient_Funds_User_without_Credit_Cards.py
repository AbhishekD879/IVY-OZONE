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
class Test_C29026_Insufficient_Funds_User_without_Credit_Cards(Common):
    """
    TR_ID: C29026
    NAME: Insufficient Funds User without Credit Cards
    DESCRIPTION: This test case verifies the absence of Quick Deposit section and presence of Insufficient Funds Error message for the User with no registered Credit Cards
    PRECONDITIONS: 1. User account with **0 balance and NO registered Credit Cards** (additional pop-up Quick Deposit)
    PRECONDITIONS: 2. User account with **positive balance but NO registered Credit Cards**
    """
    keep_browser_open = True

    def test_001_log_in_with_user_account_from_preconditions___1(self):
        """
        DESCRIPTION: Log in with user account (from preconditions - #1)
        EXPECTED: - User is logged in
        """
        pass

    def test_002_add_any_selection_to_the_bet_slip_and_open_the_bet_slippagewidget(self):
        """
        DESCRIPTION: Add any selection to the Bet Slip and open the Bet Slip page/widget
        EXPECTED: - Made selection is displayed correctly within Bet Slip content area
        """
        pass

    def test_003_enter_stake___anyand_tap_place_bet_button(self):
        """
        DESCRIPTION: Enter 'Stake' :
        DESCRIPTION: - any
        DESCRIPTION: and tap 'PLACE BET' button
        EXPECTED: - 'QUICK DEPOSIT' section is not displayed
        EXPECTED: - Betslip is closed
        EXPECTED: - User is navigated to 'Deposit' page, 'Add Credit/Debit Cards' tab for **Coral** brand
        EXPECTED: * User is navigated to Account One system for **Ladbrokes** brand
        """
        pass

    def test_004_log_out_of_the_app_and_log_in_with_user_account_from_preconditions___2(self):
        """
        DESCRIPTION: Log out of the app and Log in with user account (from preconditions - #2)
        EXPECTED: 
        """
        pass

    def test_005_clear_betslip_and_then_add_any_selection_to_the_bet_slip_and_open_the_bet_slippagewidget(self):
        """
        DESCRIPTION: Clear Betslip and then add any selection to the Bet Slip and open the Bet Slip page/widget
        EXPECTED: - Made selection is displayed correctly within Bet Slip content area
        """
        pass

    def test_006_enter_stake___greater_than_user_balanceand_tap_place_bet_button(self):
        """
        DESCRIPTION: Enter 'Stake' :
        DESCRIPTION: - greater than user balance
        DESCRIPTION: and tap 'PLACE BET' button
        EXPECTED: Expected Result should match ER from step 3
        """
        pass
