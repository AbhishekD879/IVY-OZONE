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
class Test_C59898494_Verify_the_undo_button__2_single_OA_bets_and_counter_offer_received_for_both_User_clicks_on_remove_button_for_one_of_them_uses_the_undo_button_to_undo_his_her_actions_and_then_accepts_the_offer(Common):
    """
    TR_ID: C59898494
    NAME: Verify the undo button - 2 single OA bets and counter offer received for both. User clicks on remove button for one of them, uses the undo button to undo his/her actions and then accepts the offer
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_two_single__selections__to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add two single  selections  to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_counter_offer_by_price_for_both_singles(self):
        """
        DESCRIPTION: Counter offer by price for both singles
        EXPECTED: Counter offer with the new prices highlighted and updated potential returns shown  to the customer
        """
        pass

    def test_003_verify_undo_button(self):
        """
        DESCRIPTION: Verify Undo button
        EXPECTED: Counter offer should show the remove button and then when clicked for one selection, should show the undo button.
        EXPECTED: Clicking on undo will put the counter offer back into its original state and clicking on the accept button should successfully place both bets.
        EXPECTED: The bet receipt, My Bets and Account History should show both bets in My Bets and Account History.
        """
        pass
