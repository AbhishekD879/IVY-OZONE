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
class Test_C59898458_Acca_5_Sports_Bet_Accepted(Common):
    """
    TR_ID: C59898458
    NAME: Acca 5 Sports Bet Accepted
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_five_selections_from_any_sport_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add five selections from any sport to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_accept_the_bet_in_ob_ti_tool(self):
        """
        DESCRIPTION: Accept the bet in OB TI Tool
        EXPECTED: Bet is placed and the customer is taken to the bet receipt
        EXPECTED: My Bets and Account History should show the bet.
        """
        pass
