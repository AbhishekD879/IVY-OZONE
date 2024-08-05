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
class Test_C59898473_Price_update_during_Overask_Review_Process(Common):
    """
    TR_ID: C59898473
    NAME: Price update during Overask Review Process
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

    def test_002_update_the_price_in_ob_during_overask_review_process(self):
        """
        DESCRIPTION: Update the price in OB during Overask Review Process
        EXPECTED: Updated price should not be shown in betslip
        EXPECTED: If counter offer is made in TI  then the bet should appear in the state sent back from TI
        EXPECTED: No error messaging regarding price change should be shown
        """
        pass
