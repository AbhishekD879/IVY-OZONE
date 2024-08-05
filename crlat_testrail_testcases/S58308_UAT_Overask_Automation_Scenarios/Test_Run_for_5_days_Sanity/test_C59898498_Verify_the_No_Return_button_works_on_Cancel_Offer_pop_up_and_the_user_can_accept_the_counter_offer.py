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
class Test_C59898498_Verify_the_No_Return_button_works_on_Cancel_Offer_pop_up_and_the_user_can_accept_the_counter_offer(Common):
    """
    TR_ID: C59898498
    NAME: Verify the 'No, Return' button works on Cancel Offer pop up and the user can accept the counter offer
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
        EXPECTED: Counter offer with the new stake highlighted on FE
        """
        pass

    def test_003_verify_the_no_return_button(self):
        """
        DESCRIPTION: Verify the 'No, Return' button
        EXPECTED: When user clicks on the Cancel button, they should see the Cancel Offer pop up.
        EXPECTED: On pressing the 'No, Return' button, they should be taken back to the counter offer and pressing the Accept button should take them to bet receipt.
        EXPECTED: My Bets and Account History should show this bet.
        """
        pass
