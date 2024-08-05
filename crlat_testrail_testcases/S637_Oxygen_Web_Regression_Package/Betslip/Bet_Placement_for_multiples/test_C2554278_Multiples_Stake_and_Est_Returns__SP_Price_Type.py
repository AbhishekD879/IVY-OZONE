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
class Test_C2554278_Multiples_Stake_and_Est_Returns__SP_Price_Type(Common):
    """
    TR_ID: C2554278
    NAME: Multiples Stake and Est. Returns - SP Price Type
    DESCRIPTION: AUTOTEST: [C2554301]
    DESCRIPTION: This test case verifies calculations of 'Stake', 'Est. Returns', 'Total Stake' and 'Total Est. Returns' fields for Multiples
    DESCRIPTION: *Note:* Multiples may not be available after adding Special events to the Betslip
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_several_selections_with_sp_price_type_from_different_race_events_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections with 'SP' price type from different <Race> events to the Betslip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_002_go_to_betslip__multiples_section(self):
        """
        DESCRIPTION: Go to Betslip-> 'Multiples' section
        EXPECTED: 
        """
        pass

    def test_003_verify_est_returns(self):
        """
        DESCRIPTION: Verify 'Est. Returns'
        EXPECTED: 'Est. Returns' field contains "N/A"
        """
        pass

    def test_004_verify_total_stake_field(self):
        """
        DESCRIPTION: Verify 'Total Stake' field
        EXPECTED: 'Total Stake' = £0.00
        """
        pass

    def test_005_verify_total_est_returns_field(self):
        """
        DESCRIPTION: Verify 'Total Est. Returns' field
        EXPECTED: 'Total Est. Returns' = £0.00
        EXPECTED: **From OX99**
        EXPECTED: Name for 'Total Est. Returns' is changed:
        EXPECTED: Coral: **'Estimated Returns'**
        EXPECTED: Ladbrokes: **'Potential Returns'**
        """
        pass

    def test_006_enter_stake_for_at_least_one_of_available_multiple_types(self):
        """
        DESCRIPTION: Enter 'Stake' for at least one of available Multiple Types
        EXPECTED: * **'Total Stake'** field corresponds to entered 'Stake' multiplied by the number of bets included in a Multiple Type.
        EXPECTED: * **'Est. Returns'** and **'Total Est. Returns'** contain "N/A"
        """
        pass
