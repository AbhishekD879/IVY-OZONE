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
class Test_C434202_Odds_N_A_for_a_Multiple_Type_with_an_SP_price_selection(Common):
    """
    TR_ID: C434202
    NAME: Odds N/A for a Multiple Type with an SP price selection
    DESCRIPTION: This test case verifies displaying N/A odds for a Multiple in case if one of the selections contains Races event (SP price only)
    PRECONDITIONS: 1. In order to check the potential payout value for multiple bets please go to Dev Tools->Network->All->buildBet->payout:
    PRECONDITIONS: * For Win Only bets the value with the legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: * For each way bets the sum of the value for legType="P" and the value for legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: <potential="#.#" legType="P"/>
    """
    keep_browser_open = True

    def test_001_add_two_selections_from_different_events_to_the_betslip_one_of_which_is_from_races_with_sp_price(self):
        """
        DESCRIPTION: Add two selections from different events to the Betslip one of which is from Races with SP price
        EXPECTED: Events are added to the Betslip
        """
        pass

    def test_002_go_to_betslip_multiples_section(self):
        """
        DESCRIPTION: Go to Betslip->'Multiples' section
        EXPECTED: * Multiples are available for added selections
        EXPECTED: * Odds and 'Est. Returns' value for a Multiple Type Double(1) is 'N/A'
        """
        pass

    def test_003_enter_stake_for_available_multiple_type_and_check_received_potential_payout_value(self):
        """
        DESCRIPTION: Enter 'Stake' for available Multiple Type and check received potential payout value
        EXPECTED: * 'Total Est. Returns' field contains "N/A"
        EXPECTED: * Potential payout values is NOT received in response for an appropriate Multiple Type
        """
        pass

    def test_004_add_one_or_more_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add one or more selections to the Betslip
        EXPECTED: Events are added to the Betslip
        """
        pass

    def test_005_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: **Before OX99**
        EXPECTED: * Place your ACCA section is displayed with corresponding Multiple Type (Treble/Accumulator) on the top of the Betslip (**From OX99** TREBLE is on the top of 'Multiples' section)
        EXPECTED: * Odds and 'Est. Returns' value for a Multiple Type (Treble/Accumulator) is 'N/A'
        """
        pass

    def test_006_enter_stake_for_treblr_and_check_received_potential_payout_value(self):
        """
        DESCRIPTION: Enter 'Stake' for TREBLR and check received potential payout value
        EXPECTED: * 'Total Est. Returns' field contains "N/A" (**From OX99** Coral: 'Estimated Returns'; Ladbrokes: 'Potential Returns')
        EXPECTED: * Potential payout value is NOT received in response for an appropriate Multiple Type
        """
        pass
