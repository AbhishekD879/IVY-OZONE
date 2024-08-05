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
class Test_C22533605_Verify_Acca_Bar_displaying_when_adding_selections_with_different_price_type_SP_and_LP(Common):
    """
    TR_ID: C22533605
    NAME: Verify Acca Bar displaying when adding selections  with different price type (SP and LP)
    DESCRIPTION: This test case verifies Acca Bar displaying when adding selections  with different price type (SP and LP)
    DESCRIPTION: Odds calculation on ACCA Bar instruction: https://confluence.egalacoral.com/display/SPI/Odds+calculation+on+ACCA+notification
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. User should be logged in
    PRECONDITIONS: 3. Go to My Account menu -> Settings
    PRECONDITIONS: 4. Choose Fractional price format
    """
    keep_browser_open = True

    def test_001_add_at_least_two_selections_from_different_events_to_the_betslip_but_with_different_price_type_sp_and_lp(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip but with different price type (SP and LP)
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Bar doesn't appear
        """
        pass

    def test_002_verify_potential_payout_parameter_in_buildbet_response(self):
        """
        DESCRIPTION: Verify 'potential payout' parameter in 'buildBet' response
        EXPECTED: 'potential payout' parameter is NOT received at all in 'buildBet' response
        """
        pass
