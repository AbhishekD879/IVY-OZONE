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
class Test_C18636167_Verify_Acca_Bar_for_Fractional_price_format(Common):
    """
    TR_ID: C18636167
    NAME: Verify Acca Bar for Fractional price format
    DESCRIPTION: This test case verifies Acca Bar for Fractional price format.
    DESCRIPTION: Odds calculation on ACCA Bar instruction: https://confluence.egalacoral.com/display/SPI/Odds+calculation+on+ACCA+notification
    PRECONDITIONS: 1. Load app
    PRECONDITIONS: 2. User should be logged in
    PRECONDITIONS: 3. Go to My Account menu -> Settings
    PRECONDITIONS: 4. Choose Fractional price format
    """
    keep_browser_open = True

    def test_001_add_at_least_two_selections_from_different_events_to_the_betslip_where_potential_payout_parameter_is_less_than_101(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip where potential payout parameter is less than 1.01
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Bar appears
        EXPECTED: * Value on ACCA Bar is displayed in the next format:
        EXPECTED: 1/1000
        """
        pass

    def test_002_add_at_least_two_selections_from_different_events_to_the_betslip_where_potential_payout_parameter_is_equal_or_higher_101(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip where potential payout parameter is equal or higher 1.01
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Bar appears
        EXPECTED: * Value on ACCA Bar is displayed in the next format:
        EXPECTED: #.##/# (e.g. 0.01/1)
        """
        pass
