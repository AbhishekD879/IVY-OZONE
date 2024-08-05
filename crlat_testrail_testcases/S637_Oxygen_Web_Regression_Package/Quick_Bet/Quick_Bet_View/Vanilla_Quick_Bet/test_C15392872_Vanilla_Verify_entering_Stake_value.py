import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C15392872_Vanilla_Verify_entering_Stake_value(Common):
    """
    TR_ID: C15392872
    NAME: [Vanilla] Verify entering 'Stake' value
    DESCRIPTION: This test case verifies entering stake value in a 'Stake' field using numeric keyboard for Quick Bet
    PRECONDITIONS: Oxygen application is loaded
    """
    keep_browser_open = True

    def test_001_select_one_sportraces_selection(self):
        """
        DESCRIPTION: Select one <Sport>/<Races> selection
        EXPECTED: * Quick Bet is opened
        EXPECTED: * Added selection is displayed
        EXPECTED: * Numeric keyboard is collapsed by default
        """
        pass

    def test_002_tap_on_stake_field(self):
        """
        DESCRIPTION: Tap on 'Stake' field
        EXPECTED: * Stake field is focused
        EXPECTED: * '<currency symbol>' is shown within box --!!! on sports-hl.coral.co.uk this is obsolete, no currency symbol within field, but the "stake" text is present
        EXPECTED: * Numeric keyboard is opened with slide-in animation
        EXPECTED: * Quick stakes are NOT displayed when the numeric keyboard is opened
        EXPECTED: * 'ADD TO BETSLIP' buttons is enabled
        EXPECTED: * 'PLACE BET' button is disabled
        EXPECTED: ![](index.php?/attachments/get/31329)
        """
        pass

    def test_003_in_stake_field_enter_numeric_values(self):
        """
        DESCRIPTION: In stake field enter numeric values
        EXPECTED: * Entered numbers are displayed in the 'Stake' field
        EXPECTED: * 'Total Stake' and 'Estimated Returns' are changed according to the formula
        EXPECTED: * 'ADD TO BETSLIP' buttons is enabled
        EXPECTED: * 'PLACE BET' button becomes enabled
        """
        pass

    def test_004_tap_remove_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Remove' button on numeric keyboard
        EXPECTED: * Last entered symbol is deleted from 'Stake' field
        EXPECTED: *  '.' button on keyboard is greyed out (disabled) after removing the last digit of value (e.g. XX.X*X*)
        EXPECTED: *  '.' button on keyboard becomes enabled once ".X" value is removed  (e.g. XX*.X*)
        """
        pass

    def test_005_in_stake_field_enter_numeric_values_by_using_quick_stakes_buttons(self):
        """
        DESCRIPTION: In stake field enter numeric values by using 'Quick stakes' buttons
        EXPECTED: * Entered numbers are displayed in the 'Stake' field
        EXPECTED: * 'Total Stake'' and 'Estimated Returns' are changed according to the formula
        EXPECTED: * 'ADD TO BETSLIP' and PLACE BET' buttons are enabled
        """
        pass

    def test_006_tap_remove_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Remove' button on numeric keyboard
        EXPECTED: * Last entered symbol is deleted from 'Stake' field
        EXPECTED: *  '.' button on keyboard is greyed out (disabled) after removing the last digit of value (e.g. XX.X*X*)
        EXPECTED: *  '.' button on keyboard becomes enabled once ".X" value is removed  (e.g. XX*.X*)
        """
        pass

    def test_007_enter_value_more_than_max_allowed_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value more than max allowed  value in 'Stake' field
        EXPECTED: * XXX,XXX,XXX,XXX.XX is the max value limitations for Stake field.
        EXPECTED: * It is impossible to enter more than 12 digits and 2 decimals in 'Stake' field.
        """
        pass

    def test_008_tap_return_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Return' button on numeric keyboard
        EXPECTED: * Stake field is NOT focused
        EXPECTED: * '<currency symbol> stake value' is shown within box
        EXPECTED: * Numeric keyboard is NOT shown
        """
        pass

    def test_009_set_cursor_over_stake_field_again(self):
        """
        DESCRIPTION: Set cursor over 'Stake' field again
        EXPECTED: * 'Stake' field is focused
        EXPECTED: * Numeric keyboard is shown
        EXPECTED: *  '<currency symbol> stake value' remains shown within box
        EXPECTED: *  When user enters new value > new value is shown instead of an old one
        EXPECTED: *  When user taps 'Remove' on keyboard > each digit is removed one by one
        """
        pass

    def test_010_enter_value_under_1_in_decimal_format(self):
        """
        DESCRIPTION: Enter value under 1 in decimal format
        EXPECTED: * 'Stake' field is automatically filled value in decimal format (e.g. '.2 = 0.2')
        EXPECTED: * '.' button becomes greyed out (disabled) on keyboard
        """
        pass

    def test_011_log_in_and_repeat_steps_1_9_for_all_currencies(self):
        """
        DESCRIPTION: Log in and repeat steps #1-9 for all currencies
        EXPECTED: Results are the same
        """
        pass
