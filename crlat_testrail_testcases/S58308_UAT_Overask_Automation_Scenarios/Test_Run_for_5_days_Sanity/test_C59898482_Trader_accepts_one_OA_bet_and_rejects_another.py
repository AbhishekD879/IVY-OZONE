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
class Test_C59898482_Trader_accepts_one_OA_bet_and_rejects_another(Common):
    """
    TR_ID: C59898482
    NAME: Trader accepts one OA bet and rejects another
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_two_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add two selections to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_accepts_one_oa_bet_and_reject_another_in_ob_ti(self):
        """
        DESCRIPTION: Accepts one OA bet and reject another in OB TI
        EXPECTED: Customer should see bet receipt showing that one bet was placed and the other was not - message showing "Trader did not accept the bet".
        EXPECTED: Only the accepted bet should be seen in both My Bets and Account History.
        """
        pass
