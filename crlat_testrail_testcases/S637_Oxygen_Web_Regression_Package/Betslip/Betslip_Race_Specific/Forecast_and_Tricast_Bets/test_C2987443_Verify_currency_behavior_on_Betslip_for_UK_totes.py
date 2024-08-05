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
class Test_C2987443_Verify_currency_behavior_on_Betslip_for_UK_totes(Common):
    """
    TR_ID: C2987443
    NAME: Verify currency behavior on Betslip for UK totes
    DESCRIPTION: This test case verifies the user currency and pool currency on Betslip for UK tote pools for users with different currency than pool currency.
    PRECONDITIONS: 1. User is logged in with different currency than pool one
    PRECONDITIONS: 2. User balance is enough to place a bet
    PRECONDITIONS: 3. User in on any UK tote pool (Win/Place/Execta/Trifecta...) race card.
    """
    keep_browser_open = True

    def test_001_choose_any_active_selection_from_any_pool_available_winplaceexectatrifecta_and_add_it_to_betslip(self):
        """
        DESCRIPTION: Choose any active selection from any pool available (Win/Place/Execta/Trifecta...) and add it to betslip
        EXPECTED: * Selection is successfully added to betslip
        EXPECTED: * Betslip counter is increased by 1 item
        """
        pass

    def test_002_click_on_betslip_and_verify_the_stake_and_total_stake_currency_sign(self):
        """
        DESCRIPTION: Click on Betslip and verify the Stake and Total stake currency sign
        EXPECTED: * Stake value currency is displayed in Pool currency and pool Currency Sign
        EXPECTED: * Total stake value currency is displayed in User currency and user Currency Sign
        """
        pass

    def test_003_enter_any_value_into_stake_value_input_field(self):
        """
        DESCRIPTION: Enter any value into stake value input field
        EXPECTED: * Stake value currency is displayed in Pool currency and pool Currency Sign
        EXPECTED: * Total stake value currency is displayed in User currency and user Currency Sign
        """
        pass

    def test_004_add_few_selections_from_1_pool_to_betslip_and_verify_currency_signs(self):
        """
        DESCRIPTION: Add few selections from 1 pool to betslip and verify currency signs
        EXPECTED: * Stake value currency is displayed in Pool currency and pool Currency Sign
        EXPECTED: * Total stake value currency is displayed in User currency and user Currency Sign
        """
        pass
