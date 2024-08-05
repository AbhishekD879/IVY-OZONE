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
class Test_C59898464_Single_Football_Bet_placed_using_money_and_free_bet_Countered_by_Stake(Common):
    """
    TR_ID: C59898464
    NAME: Single Football Bet placed using money and free bet Countered by Stake
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    PRECONDITIONS: Customer should have Freebets in the account
    """
    keep_browser_open = True

    def test_001_add_single_football__selection_to_betslip_and_place_bet_using_money_and_free_bet(self):
        """
        DESCRIPTION: Add Single Football  selection to betslip and place bet using money and free bet
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_counter_by_stake_in_ob_ti_tool(self):
        """
        DESCRIPTION: Counter by stake in OB TI tool
        EXPECTED: On FE Customer should see the bet slip with a message saying that free bet cannot be used.
        EXPECTED: No bet is placed and no bet shows in My Bets and Account History.
        """
        pass
