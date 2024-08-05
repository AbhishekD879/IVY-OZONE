import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C23820446_Vanilla_Quick_Bet__Verify_entering_CVV_and_Amount_value(Common):
    """
    TR_ID: C23820446
    NAME: [Vanilla]- Quick Bet - Verify entering 'CVV' and 'Amount' value
    DESCRIPTION: This test case verifies entering stake value in a 'CVV' and 'Amount' fields using numeric keyboard for Quick Deposit within Quick Bet
    DESCRIPTION: Autotest: [C34792792]
    PRECONDITIONS: 1. Application is loaded
    PRECONDITIONS: 2. Log in under user account with positive balance
    """
    keep_browser_open = True

    def test_001_select_one_sportraces_selection(self):
        """
        DESCRIPTION: Select one <Sport>/<Races> selection
        EXPECTED: * Quick Bet is opened
        EXPECTED: * Added selection is displayed
        EXPECTED: * Numeric keyboard is collapsed by default
        """
        pass

    def test_002_enter_higher_than_user_balance_stake_and_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Enter higher than user balance stake and tap on 'Make a Deposit' button
        EXPECTED: * Quick Deposit iFrame appears
        EXPECTED: * Numeric keyboard is not shown
        EXPECTED: * 'CVV' field is empty by default
        EXPECTED: * 'Deposit Amount' field is pre-populated with amount with the difference from the balance and stake
        EXPECTED: * '-' and '+' buttons are displayed on both sides of deposit amount input field
        EXPECTED: * 'Quick Stakes' buttons are displayed below 'Deposit Amount' and 'CVV' fields
        """
        pass

    def test_003_focus_cvv_field(self):
        """
        DESCRIPTION: Focus 'CVV' field
        EXPECTED: * 'CVV' field is focused
        EXPECTED: * 'DEPOSIT AND PLACE BET' button is disabled
        """
        pass

    def test_004_enter_numeric_values(self):
        """
        DESCRIPTION: Enter numeric values
        EXPECTED: * Entered numbers are displayed in the 'CVV' field
        EXPECTED: * 'DEPOSIT AND PLACE BET' button is disabled (becomes enabled when 3 digits are entered)
        """
        pass

    def test_005_tap_remove_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Remove' button on numeric keyboard
        EXPECTED: * Last entered symbol is deleted from 'CVV' field
        """
        pass

    def test_006_tap_any_quick_stake_button_20_50_100_200(self):
        """
        DESCRIPTION: Tap any Quick Stake button
        DESCRIPTION: * 20
        DESCRIPTION: * 50
        DESCRIPTION: * 100
        DESCRIPTION: * 200
        EXPECTED: * Value in 'Deposit Amount' field is displayed according to chosen Quick Stake button value
        """
        pass

    def test_007_tap_plus_button_near_the_deposit_amount_input_field(self):
        """
        DESCRIPTION: Tap '+' button near the deposit amount input field
        EXPECTED: * The deposit amount is increased by value from Deposit amount box (user currency)
        """
        pass

    def test_008_focus_deposit_amount_field(self):
        """
        DESCRIPTION: Focus 'Deposit Amount' field
        EXPECTED: * 'Deposit Amount' field is focused
        EXPECTED: * Numeric keyboard is opened
        """
        pass

    def test_009_tap___button_near_the_deposit_amount_input_field(self):
        """
        DESCRIPTION: Tap '-' button near the deposit amount input field
        EXPECTED: * The deposit amount is decreased by value from Deposit amount box (user currency)
        """
        pass

    def test_010_log_in_and_repeat_steps_1_9_for_all_currencies_gbpusd_eur(self):
        """
        DESCRIPTION: Log in and repeat steps #1-9 for all currencies ('GBP','USD', 'EUR')
        EXPECTED: Results are the same
        """
        pass
