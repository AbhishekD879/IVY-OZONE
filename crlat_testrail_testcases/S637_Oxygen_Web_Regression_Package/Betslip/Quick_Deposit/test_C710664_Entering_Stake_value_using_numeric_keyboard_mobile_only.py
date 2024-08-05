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
class Test_C710664_Entering_Stake_value_using_numeric_keyboard_mobile_only(Common):
    """
    TR_ID: C710664
    NAME: Entering 'Stake' value using numeric keyboard (mobile only)
    DESCRIPTION: This test case verifies entering stake value in a 'Stake' field using numeric keyboard on mobile devices
    PRECONDITIONS: Oxygen application is loaded
    """
    keep_browser_open = True

    def test_001_add_sportraces_selection_to_the_bet_slip_and_navigate_to_the_betslip(self):
        """
        DESCRIPTION: Add <Sport>/<Races> selection to the Bet Slip and navigate to the BetSlip
        EXPECTED: * Bet Slip is opened
        EXPECTED: * Added selection is displayed in 'Singles' section
        """
        pass

    def test_002_verify_stake_field(self):
        """
        DESCRIPTION: Verify 'Stake' field
        EXPECTED: * Numeric keyboard isn't opened by default
        EXPECTED: * 'BET NOW'/LOG IN & BET' button is disabled
        """
        pass

    def test_003_click_on_stake_field(self):
        """
        DESCRIPTION: Click on 'Stake' field
        EXPECTED: * Stake field is focused
        EXPECTED: * '<currency symbol>' is NOT shown within box
        EXPECTED: * Numeric keyboard is opened
        """
        pass

    def test_004_in_stake_field_enter_numeric_values(self):
        """
        DESCRIPTION: In stake field enter numeric values
        EXPECTED: * Entered numbers are displayed in the 'Stake' field
        EXPECTED: * 'Estimated Returns' and 'Total Est. Returns' are changed according to the formula
        EXPECTED: * 'BET NOW'/LOG IN & BET' button becomes enabled
        """
        pass

    def test_005_tap_remove_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Remove' button on numeric keyboard
        EXPECTED: * Last entered symbol is deleted from 'Stake' field
        EXPECTED: *  '.' button on keyboard is greyed out (disabled) after removing the last digit of value (e.g. XX.X*X*)
        EXPECTED: *  '.' button on keyboard becomes enabled once ".X" value is removed  (e.g. XX*.X*)
        """
        pass

    def test_006_for_coralin_stake_field_enter_numeric_values_by_using_quick_stakes_buttonsfor_ladbrokesquick_stakes_buttons_are_not_available(self):
        """
        DESCRIPTION: For Coral:
        DESCRIPTION: In stake field enter numeric values by using 'Quick stakes' buttons
        DESCRIPTION: For Ladbrokes:
        DESCRIPTION: 'Quick stakes' buttons are not available
        EXPECTED: * Entered numbers are displayed in the 'Stake' field
        EXPECTED: * 'Estimated Returns' and 'Total Est. Returns' are changed according to the formula
        EXPECTED: * 'BET NOW'/LOG IN & BET' button becomes enabled
        """
        pass

    def test_007_tap_remove_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Remove' button on numeric keyboard
        EXPECTED: * Last entered symbol is deleted from 'Stake' field
        EXPECTED: *  '.' button on keyboard is greyed out (disabled) after removing the last digit of value (e.g. XX.X*X*)
        EXPECTED: *  '.' button on keyboard becomes enabled once ".X" value is removed  (e.g. XX*.X*)
        """
        pass

    def test_008_enter_value_more_than_max_allowed_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value more than max allowed  value in 'Stake' field
        EXPECTED: * XXX,XXX,XXX,XXX.XX is the max value limitations for Stake field.
        EXPECTED: * It is impossible to enter more than 12 digits and 2 decimals in 'Stake' field.
        """
        pass

    def test_009_tap_return_button_on_numeric_keyboardset_focus_anywhere_within_betslip(self):
        """
        DESCRIPTION: Tap 'Return' button on numeric keyboard/set focus anywhere within Betslip
        EXPECTED: * Stake field is NOT focused
        EXPECTED: * Numeric keyboard is NOT shown
        """
        pass

    def test_010_set_cursor_over_stake_field_again(self):
        """
        DESCRIPTION: Set cursor over 'Stake' field again
        EXPECTED: * 'Stake' field is focused
        EXPECTED: * Numeric keyboard is shown
        EXPECTED: *  When user enters new value > new value is shown instead of an old one
        EXPECTED: *  When user taps 'Remove' on keyboard > each digit is removed one by one
        """
        pass

    def test_011_enter_some_value__then_tap_on__button_on_keyboard__enter_some_other_value(self):
        """
        DESCRIPTION: Enter some value > then tap on '.' button on keyboard > enter some other value
        EXPECTED: * '.' button becomes greyed out (disabled)
        EXPECTED: * [Will be implemented later] X. is shown within box (once X. is entered)
        EXPECTED: * 'X.X' value is shown within box
        """
        pass

    def test_012_enter_value_under_1_in_decimal_format(self):
        """
        DESCRIPTION: Enter value under 1 in decimal format
        EXPECTED: * 'Stake' field is automatically filled value in decimal format (e.g. '.2 = 0.2')
        EXPECTED: * '.' button becomes greyed out (disabled) on keyboard
        """
        pass

    def test_013_add_at_least_two_selections_from_different_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Bet Slip
        EXPECTED: * Selections are added
        EXPECTED: * Added selections are displayed in 'Singles' section
        EXPECTED: * 'Multiples' and 'Place your ACCA' (if available) section is shown
        EXPECTED: * A list of available multiples bets is shown
        """
        pass

    def test_014_verify_all_stake_fields(self):
        """
        DESCRIPTION: Verify all 'Stake' fields
        EXPECTED: * All stake fields are NOT focused
        EXPECTED: * Numeric keyboard is NOT opened by default
        EXPECTED: * 'BET NOW'/LOG IN & BET' button is disabled
        """
        pass

    def test_015_tap_all_single_stakes_field_within_singles_section(self):
        """
        DESCRIPTION: Tap 'All single stakes' field within 'Singles' section
        EXPECTED: * Stake field becomes focused
        EXPECTED: * Numeric keyboard is opened
        EXPECTED: * 'BET NOW'/LOG IN & BET' button is disabled
        """
        pass

    def test_016_repeat_steps_3_7(self):
        """
        DESCRIPTION: Repeat steps #3-7
        EXPECTED: Results are the same
        """
        pass

    def test_017_tap_any_stake_field_within_multiples_section(self):
        """
        DESCRIPTION: Tap any 'Stake' field within 'Multiples' section
        EXPECTED: * Stake field becomes focused
        EXPECTED: * Numeric keyboard is opened
        EXPECTED: * 'BET NOW'/LOG IN & BET' button is disabled
        """
        pass

    def test_018_repeat_steps_3_7(self):
        """
        DESCRIPTION: Repeat steps #3-7
        EXPECTED: Results are the same
        """
        pass

    def test_019_na_from_ox98add_at_least_two_selections_from_same_events_to_the_bet_slip(self):
        """
        DESCRIPTION: **(N/A from OX98)**
        DESCRIPTION: Add at least two selections from same events to the Bet Slip
        EXPECTED: * Selections are added
        EXPECTED: * Added selections are displayed in 'Singles' section
        EXPECTED: * 'Forecasts/Tricasts' selection is displayed
        EXPECTED: * 'Multiples' and 'Place your ACCA' (if available) section is shown
        EXPECTED: * A list of available multiples bets is shown
        """
        pass

    def test_020_verify_from_ox_98navigate_to_forecasttricast_tabadd_forecasttricast_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: **(Verify from OX 98)**
        DESCRIPTION: Navigate to Forecast/Tricast tab
        DESCRIPTION: Add Forecast/Tricast selections to the Bet Slip
        EXPECTED: * Selections are added
        EXPECTED: * Added 'Forecasts/Tricasts' selections are displayed in 'Singles' section
        """
        pass

    def test_021_tap_any_stake_field_within_forecaststricasts_selection(self):
        """
        DESCRIPTION: Tap any 'Stake' field within 'Forecasts/Tricasts' selection
        EXPECTED: * Stake field becomes focused
        EXPECTED: * Numeric keyboard is opened
        EXPECTED: * 'BET NOW'/LOG IN & BET' button is disabled
        """
        pass

    def test_022_repeat_steps_3_7(self):
        """
        DESCRIPTION: Repeat steps #3-7
        EXPECTED: Results are the same
        """
        pass
