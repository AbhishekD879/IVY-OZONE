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
class Test_C59898499_Accept_One_Bet_Out_of_Several_Selections__make_one_OA_bet_and_two_non_OA_bets_and_the_trader_accepts_OA_bet(Common):
    """
    TR_ID: C59898499
    NAME: Accept One Bet Out of Several Selections - make one OA bet and two non OA bets and the trader accepts OA bet
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_make_one_oa_bet_and_two_non_oa_betstrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Make one OA bet and two non OA bets
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_if_trader_accepts_overask_bet(self):
        """
        DESCRIPTION: If trader accepts Overask bet
        EXPECTED: Customer should see the bet receipt with all 3 bets showing as being placed.
        EXPECTED: My Bets and Account History should reflect these bets.
        """
        pass
