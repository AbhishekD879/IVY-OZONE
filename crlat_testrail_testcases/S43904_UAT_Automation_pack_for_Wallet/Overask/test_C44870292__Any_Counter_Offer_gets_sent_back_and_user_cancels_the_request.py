import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870292__Any_Counter_Offer_gets_sent_back_and_user_cancels_the_request(Common):
    """
    TR_ID: C44870292
    NAME: - Any Counter Offer gets sent back and user cancels the request
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_an_oa_bet_and_give_any_type_of_counter_offer_in_the_ti(self):
        """
        DESCRIPTION: Place an OA bet and give any type of counter offer in the TI
        EXPECTED: The trader should have given a counter offer
        """
        pass

    def test_002_in_the_front_end_you_should_see_a_counter_offer(self):
        """
        DESCRIPTION: In the Front End, you should see a counter offer
        EXPECTED: You should see a counter offer
        """
        pass

    def test_003_click_on_the_cancel_button_in_the_counter_offer(self):
        """
        DESCRIPTION: Click on the Cancel button in the counter offer
        EXPECTED: The counter offer should have closed
        """
        pass

    def test_004_verify_that_the_bet_has_not_been_placed_by_looking_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Verify that the bet has not been placed by looking in My Bets->Open Bets
        EXPECTED: The bet should not show up in My Bets->Open Bets
        """
        pass
