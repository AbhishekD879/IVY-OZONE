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
class Test_C29039_Multiples_Stake_and_Est_Returns__LP_Price_Type(Common):
    """
    TR_ID: C29039
    NAME: Multiples Stake and Est. Returns - LP Price Type
    DESCRIPTION: AUTOTEST: C2554714
    DESCRIPTION: This test case verifies calculations of 'Stake', 'Est. Returns', 'Total Stake' and 'Total Est. Returns' fields for Multiples
    DESCRIPTION: *Note:* Multiples may not be available after adding Special events to the Betslip
    PRECONDITIONS: 1. In order to check the potential payout value for multiple bets please go to Dev Tools->Network->All->buildBet->payout:
    PRECONDITIONS: * For Win Only bets the value with the legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: * For each way bets the sum of the value for legType="P" and the value for legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: <potential="#.#" legType="P"/>
    """
    keep_browser_open = True

    def test_001_add_several_selections_with_lp_price_type_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections with 'LP' price type from different events to the Betslip
        EXPECTED: 
        """
        pass

    def test_002_go_to_betslip__multiples_section(self):
        """
        DESCRIPTION: Go to Betslip-> 'Multiples' section
        EXPECTED: * 'Multiples' section is displayed as the last section within 'Bet Slip'
        EXPECTED: * Multiples are available for added selections
        """
        pass

    def test_003_verify_est_returns_field(self):
        """
        DESCRIPTION: Verify 'Est. Returns' field
        EXPECTED: 'Est. Returns' = £0.00
        """
        pass

    def test_004_verify_total_stake_field(self):
        """
        DESCRIPTION: Verify 'Total Stake' field
        EXPECTED: Total Stake' = £0.00
        """
        pass

    def test_005_verify_total_est_returns_field(self):
        """
        DESCRIPTION: Verify 'Total Est. Returns' field
        EXPECTED: 'Total Est. Returns' = £0.00
        EXPECTED: **From OX99**
        EXPECTED: Name for 'Total Est. Returns' is changed:
        EXPECTED: Coral: **'Estimated Returns'**
        EXPECTED: Ladbrokes: **'Potential Returns'**
        """
        pass

    def test_006_enter_stake_for_one_of_available_multiple_types_and_check_received_potential_payout_valueautomated_partially(self):
        """
        DESCRIPTION: Enter 'Stake' for one of available Multiple Types and check received potential payout value
        DESCRIPTION: #automated partially
        EXPECTED: * **'Total Stake'** field corresponds to entered 'Stake' multiplied by the number of bets included in a Multiple Type.
        EXPECTED: * 'Est. Returns' and 'Total Est. Returns' are calculated for this Multiple Type
        EXPECTED: * Potential payout value is received in response for appropriate Multiple Type
        EXPECTED: * **'Est. Returns'** and **'Total Est. Returns'** values on front-end correspond to Potential payout value
        """
        pass

    def test_007_enter_stake_for_a_few_of_available_multiple_typesnot_automated(self):
        """
        DESCRIPTION: Enter 'Stake' for a few of available Multiple Types
        DESCRIPTION: #not automated
        EXPECTED: * **'Total Stake'** field is a sum of all entered 'Stakes' multiplied by the number of bets included in a Multiple Type.
        EXPECTED: * **'Total Est. Returns'** field is a sum of all 'Est. Returns'.
        """
        pass
