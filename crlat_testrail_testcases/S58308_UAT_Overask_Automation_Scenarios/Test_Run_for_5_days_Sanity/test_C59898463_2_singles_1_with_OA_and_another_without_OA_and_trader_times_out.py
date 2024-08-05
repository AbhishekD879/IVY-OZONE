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
class Test_C59898463_2_singles_1_with_OA_and_another_without_OA_and_trader_times_out(Common):
    """
    TR_ID: C59898463
    NAME: 2 singles: 1 with OA and another without OA and trader times out
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_two_selections_from_any_sport_to_betslip_one_with_overask_and_another_without_overasktrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add two selections from any sport to Betslip (one with overask and another without overask)
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_time_out_in_ti(self):
        """
        DESCRIPTION: Time out in TI
        EXPECTED: After the Counter Offer has expired in TI, the customer should see an automated offer at max stake in bet slip
        """
        pass
