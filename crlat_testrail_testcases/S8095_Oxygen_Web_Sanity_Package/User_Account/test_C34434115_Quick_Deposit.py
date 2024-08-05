import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C34434115_Quick_Deposit(Common):
    """
    TR_ID: C34434115
    NAME: Quick Deposit
    DESCRIPTION: This test case verifies Successful Depositing and Placing Bet functionality on the Betslip page via credit/debit cards.
    DESCRIPTION: AUTOMATED [C45273007]
    PRECONDITIONS: * User account with at least one available previously added credit card
    PRECONDITIONS: * Make sure that user has 3DS Card added to the account https://confluence.egalacoral.com/display/SPI/How+to+create+test+user+for+GVC+Vanilla+automatically+by-passing+KYC
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_with_user_account_from_preconditions(self):
        """
        DESCRIPTION: Log in with user account (from preconditions)
        EXPECTED: User is logged in
        """
        pass

    def test_003_add_any_selection_to_the_betslip_and_open_betslip_page__widget(self):
        """
        DESCRIPTION: Add any selection to the Betslip and open Betslip page  / widget
        EXPECTED: Added selections are displayed within Betslip content area
        """
        pass

    def test_004_enter_stake_which_exceeds_current_user_balance(self):
        """
        DESCRIPTION: Enter 'Stake' which exceeds current user balance
        EXPECTED: * 'Please deposit a min of £XX.XX to continue placing your bet' red message is displayed in Betslip
        EXPECTED: * 'Make a deposit' button is shown and enabled
        """
        pass

    def test_005_press_make_a_deposit_button(self):
        """
        DESCRIPTION: Press 'Make a deposit' button
        EXPECTED: * 'Quick deposit' feature appears in Betslip
        EXPECTED: ![](index.php?/attachments/get/11806968)
        """
        pass

    def test_006_enter_valid_cvv_into_cvv2_field_and_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Enter valid CVV into 'CVV2' field and tap 'DEPOSIT & PLACE BET' button
        EXPECTED: * User balance is updated and calculated as:
        EXPECTED: (User Balance before deposit) + (Amount of deposit) - (Stake of placed bet)
        EXPECTED: * Bet is placed (If no pop-ups are displayed to user)
        EXPECTED: * Betslip is replaced with a Bet Receipt view
        """
        pass
