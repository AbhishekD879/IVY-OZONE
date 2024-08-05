import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870290__Acca_4_Sports_Bet_timed_out_in_TI(Common):
    """
    TR_ID: C44870290
    NAME: - Acca 4 Sports Bet timed out in TI
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_four_selections_from_any_sport_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add four selections from any sport to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_time_out_in_ti(self):
        """
        DESCRIPTION: Time out in TI
        EXPECTED: After the Counter Offer has expired in TI, the customer will see the bet slip with the message that "this bet has not been accepted by traders!" and we should not see a bet in My Bets and Account History.
        """
        pass
