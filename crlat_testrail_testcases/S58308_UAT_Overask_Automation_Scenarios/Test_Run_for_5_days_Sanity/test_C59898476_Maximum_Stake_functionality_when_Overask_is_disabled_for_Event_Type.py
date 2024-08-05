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
class Test_C59898476_Maximum_Stake_functionality_when_Overask_is_disabled_for_Event_Type(Common):
    """
    TR_ID: C59898476
    NAME: Maximum Stake functionality when Overask is disabled for Event Type
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    PRECONDITIONS: In OB go to any sport(Ex -Football -->  Premier league ) disable BI check box at Type level
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow should not be triggered instead Customer should see a message showing the max stake
        """
        pass
