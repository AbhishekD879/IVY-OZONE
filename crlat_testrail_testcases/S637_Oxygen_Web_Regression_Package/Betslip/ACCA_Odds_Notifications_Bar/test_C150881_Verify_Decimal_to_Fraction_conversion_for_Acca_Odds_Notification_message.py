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
class Test_C150881_Verify_Decimal_to_Fraction_conversion_for_Acca_Odds_Notification_message(Common):
    """
    TR_ID: C150881
    NAME: Verify Decimal to Fraction conversion for Acca Odds Notification message
    DESCRIPTION: This test case verifies Decimal to Fraction conversion for Acca Odds Notification message.
    DESCRIPTION: Odds calculation on ACCA notification instruction: https://confluence.egalacoral.com/display/SPI/Odds+calculation+on+ACCA+notification
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. User should be logged in
    PRECONDITIONS: 3. Go to My account menu -> Settings
    PRECONDITIONS: 4. Choose Fraction price format
    """
    keep_browser_open = True

    def test_001_add_at_least_two_selections_from_different_events_to_the_betslip_where_potential_payout_parameter_is_equal_to_value_in_decimal_odds_column_of_attached_table(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip where potential payout parameter is equal to value in 'Decimal Odds' column of attached table
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Odds Notification message appears
        """
        pass

    def test_002_verify_potential_payout_parameter_from_the_network___buildbet_response___bets___appropriate_multiple_id(self):
        """
        DESCRIPTION: Verify potential payout parameter from the Network -> buildBet response -> bets -> appropriate multiple id
        EXPECTED: * Potential payout parameter has particular value from 'Decimal Odds' column of attached table
        EXPECTED: * Potential payout value is displayed in Decimal format
        """
        pass

    def test_003_verify_decimal_to_fraction_conversion_for_acca_odds_notification_message_for_value_from_steps_2(self):
        """
        DESCRIPTION: Verify Decimal to Fraction conversion for ACCA Odds Notification message for value from steps 2
        EXPECTED: * Price on Acca Odds Notification message is displayed in Fractional format
        EXPECTED: * Price on Acca Odds Notification message is equal to values in 'Fractional Odds' column that corresponds to appropriate 'Decimal Odds' column
        EXPECTED: * Price on Acca Odds Notification message is displayed in the next format: #/#;
        """
        pass

    def test_004_verify_decimal_to_fraction_conversion_for_acca_odds_notification_message_for_all_values_from_attached_table(self):
        """
        DESCRIPTION: Verify Decimal to Fraction conversion for ACCA Odds Notification message for all values from attached table
        EXPECTED: * Price on Acca Odds Notification message is displayed in Fractional format
        EXPECTED: * Price on Acca Odds Notification message is equal to values in 'Fractional Odds' column that corresponds to appropriate 'Decimal Odds' column
        EXPECTED: * Price on Acca Odds Notification message is displayed in the next format: #/#;
        """
        pass

    def test_005_add_at_least_two_selections_from_different_events_to_the_betslip_where_potential_payout_parameter_in_the_buildbet_response_corresponds_to_values_from_minimummaximum_rounding_value_columns(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip where potential payout parameter in the buildBet response corresponds to values from 'Minimum/Maximum rounding value' columns
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Odds Notification message appears
        """
        pass

    def test_006_verify_decimal_to_fraction_conversion_for_acca_odds_notification_message(self):
        """
        DESCRIPTION: Verify Decimal to Fraction conversion for ACCA Odds Notification message
        EXPECTED: * Price on Acca Odds Notification message is displayed in Fractional format
        EXPECTED: * If potential payout decimal value < 10, see Odds ladder in the attachment
        EXPECTED: * If potential payout decimal value > 10, numerator value is potential payout field in the buildBet response minus 1, denumerator value is 1 on Acca Odds Notification message
        EXPECTED: * Price on Acca Odds Notification message is displayed in the next format: #/#
        """
        pass

    def test_007_change_price_format_to_decimal_in_my_account_menu___settings(self):
        """
        DESCRIPTION: Change price format to Decimal in My account menu -> Settings
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_1_7_but_verify_displaying_prices_in_decimal_format_on_acca_odds_notification_message(self):
        """
        DESCRIPTION: Repeat steps 1-7 but verify displaying prices in Decimal format on ACCA Odds Notification message
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Odds Notification message appears
        EXPECTED: * Payout parameter from the buildBet response is displayed on ACCA Odds Notification message as Odds in the next format: #.##
        """
        pass
