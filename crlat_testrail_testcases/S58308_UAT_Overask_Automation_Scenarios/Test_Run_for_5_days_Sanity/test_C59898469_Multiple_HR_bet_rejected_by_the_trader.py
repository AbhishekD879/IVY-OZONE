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
class Test_C59898469_Multiple_HR_bet_rejected_by_the_trader(Common):
    """
    TR_ID: C59898469
    NAME: Multiple HR bet rejected by the trader
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_mutliple_hr_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add mutliple HR selections to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_reject_the_multiple_bet_in_ob_ti_tool(self):
        """
        DESCRIPTION: Reject the multiple bet in OB TI Tool
        EXPECTED: Customer sees a Trader has not accepted the bet message in betslip. No bet should be seen in My Bets and Account History
        """
        pass