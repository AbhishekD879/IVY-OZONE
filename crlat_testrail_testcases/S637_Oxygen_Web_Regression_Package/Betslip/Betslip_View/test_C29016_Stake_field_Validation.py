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
class Test_C29016_Stake_field_Validation(Common):
    """
    TR_ID: C29016
    NAME: 'Stake' field Validation
    DESCRIPTION: This test case is for checking validation in a 'Stake' field
    DESCRIPTION: This test case applies for **Mobile** and **Tablet** application.
    PRECONDITIONS: - User is logged in with positive balance
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sportraces_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport>/<Races> icon from the sports menu ribbon
        EXPECTED: <Sport>/<Races> landing page is opened
        """
        pass

    def test_003_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the BetSlip
        EXPECTED: - BetSlip counter is increased
        EXPECTED: - Selected price button is highlighted in green
        """
        pass

    def test_004_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the BetSlip
        EXPECTED: - Bet Slip is opened with selection selected
        EXPECTED: - Numeric keyboard is NOT available above 'BET NOW'/'LOG IN & BET' button (From OX 100)
        """
        pass

    def test_005_verify_default_value_in_stake_field(self):
        """
        DESCRIPTION: Verify default value in 'Stake' field
        EXPECTED: - Stake field is empty
        """
        pass

    def test_006_tap_on_betslip_in_any_place_except_the_keypad(self):
        """
        DESCRIPTION: Tap on Betslip in any place except the keypad
        EXPECTED: - Numeric keypad is closed (on devices)
        EXPECTED: - Stake field has default value "Stake" pre-populated (Actual from OX99)
        """
        pass

    def test_007_tap_on_stake_field_and_enter_numeric_values(self):
        """
        DESCRIPTION: Tap on stake field and enter numeric values
        EXPECTED: - Entered numbers are displayed in the 'Stake' field + Currency sign is shown (Actual from OX99)
        EXPECTED: - 'Estimated Returns' and 'Total Est. Returns/Total Potential Returns' are changed accordingly
        """
        pass

    def test_008_enter_value_under_1_in_decimal_format(self):
        """
        DESCRIPTION: Enter value under 1 in decimal format
        EXPECTED: 'Stake' field is automatically filled value in decimal format (e.g. '.2 = 0.2')
        """
        pass

    def test_009_enter_value_more_than_max_allowed_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value more than max allowed  value in 'Stake' field.
        EXPECTED: - XXX,XXX,XXX,XXX.XX is the max value limitations for Stake field
        EXPECTED: - It is impossible to enter more than 12 digits and 2 decimals in 'Stake' field.
        """
        pass

    def test_010_add_at_least_two_selections_from_different_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_011_repeat_steps_7_9_for_all_stakes_field_within_singles_section_coral_only(self):
        """
        DESCRIPTION: Repeat steps #7-9 for 'All Stakes' field within 'Singles' section [CORAL ONLY]
        EXPECTED: Validation rules are the same as above
        """
        pass

    def test_012_go_to_bet_slipmultiples_section(self):
        """
        DESCRIPTION: Go to Bet Slip,'Multiples' section
        EXPECTED: A list of available multiples bets is shown
        """
        pass

    def test_013_repeat_steps_7_9(self):
        """
        DESCRIPTION: Repeat steps #7-9
        EXPECTED: Validation rules are the same as above
        """
        pass

    def test_014_repeat_steps_7_9_for_forecast__tricast_bets(self):
        """
        DESCRIPTION: Repeat steps #7-9 for 'Forecast / Tricast' bets
        EXPECTED: Validation rules are the same as above
        """
        pass
