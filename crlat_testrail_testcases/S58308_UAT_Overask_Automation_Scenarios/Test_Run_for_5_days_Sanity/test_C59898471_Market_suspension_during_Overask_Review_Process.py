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
class Test_C59898471_Market_suspension_during_Overask_Review_Process(Common):
    """
    TR_ID: C59898471
    NAME: Market suspension during Overask Review Process
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_in_openbet_suspend_the_market(self):
        """
        DESCRIPTION: In Openbet, suspend the market
        EXPECTED: Suspension message is seen in betslip
        """
        pass

    def test_003_in_ti_give_a_counter_offer(self):
        """
        DESCRIPTION: In TI, give a counter offer
        EXPECTED: Customer should see a bet not accepted by trader message on FE
        """
        pass
