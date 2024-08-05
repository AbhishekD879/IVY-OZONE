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
class Test_C59898503_Add_pre_match_and_inplay_selections_and_stake_for_higher_than_the_max_stake(Common):
    """
    TR_ID: C59898503
    NAME: Add pre match and inplay selections and stake for higher than the max stake
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_inplay_and_preplay_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add inplay and preplay selections to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: No inplay selections should be passed into the OA flow and the user should be returned the max stake messaging and no bet placed
        """
        pass
