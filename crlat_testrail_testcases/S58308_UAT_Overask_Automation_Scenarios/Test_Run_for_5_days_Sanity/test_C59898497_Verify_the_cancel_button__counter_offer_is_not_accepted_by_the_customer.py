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
class Test_C59898497_Verify_the_cancel_button__counter_offer_is_not_accepted_by_the_customer(Common):
    """
    TR_ID: C59898497
    NAME: Verify the cancel button - counter offer is not accepted by the customer
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add__selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add  selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_counter_by_stake_in_ob_ti_tool(self):
        """
        DESCRIPTION: Counter by stake in OB TI tool
        EXPECTED: Counter offer with the new stake highlighted and updated potential returns shown to the customeron FE
        """
        pass

    def test_003_verify_the_cancel_button(self):
        """
        DESCRIPTION: Verify the cancel button
        EXPECTED: On clicking Cancel -  a pop up should appear asking the customer to confirm by clicking the 'Cancel Offer' button or return to the offer by clicking on the 'No, Return button'
        EXPECTED: On clicking 'Cancel Offer', the counter offer should close.
        EXPECTED: My Bets and Account History should not show any record of this offer and cancellation.
        """
        pass
