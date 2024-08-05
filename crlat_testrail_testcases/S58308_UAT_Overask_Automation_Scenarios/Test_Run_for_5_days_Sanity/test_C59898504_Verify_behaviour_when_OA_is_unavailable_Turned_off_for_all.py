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
class Test_C59898504_Verify_behaviour_when_OA_is_unavailable_Turned_off_for_all(Common):
    """
    TR_ID: C59898504
    NAME: Verify behaviour when OA is unavailable (Turned off for all)
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is disabled(Turned off for all) for logged in user
    PRECONDITIONS: OpenBet TI--> Home --> BI Settings --> Disable Betting
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: All max bet messages should be returned and no customer should be passed into the flow
        """
        pass
