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
class Test_C59898501_Verify_the_Cancel_Offer_pop_up(Common):
    """
    TR_ID: C59898501
    NAME: Verify the Cancel Offer? pop up
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

    def test_002_counter_by_stake_in_ob_ti_tool(self):
        """
        DESCRIPTION: Counter by stake in OB TI tool
        EXPECTED: Counter offer with the new stake highlighted and updated potential returns shown to the customer on FE
        """
        pass

    def test_003_verify_the_cancel_offer_pop_up(self):
        """
        DESCRIPTION: Verify the Cancel Offer? pop up
        EXPECTED: Clicking on the Cancel button in the counter offer should initiate a Cancel Offer? pop-up.
        EXPECTED: The pop-up should have the appropriate text with "No, Return" and "Cancel" Offer buttons.
        """
        pass
