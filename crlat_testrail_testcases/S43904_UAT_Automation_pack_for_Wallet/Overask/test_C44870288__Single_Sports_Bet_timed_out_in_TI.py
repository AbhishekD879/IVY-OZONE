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
class Test_C44870288__Single_Sports_Bet_timed_out_in_TI(Common):
    """
    TR_ID: C44870288
    NAME: - Single Sports Bet timed out in TI
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_a_single_oa_bet_on_any_sport(self):
        """
        DESCRIPTION: Place a single OA bet on any sport
        EXPECTED: The bet should have gone to the OA flow
        """
        pass

    def test_002_in_the_traders_interface_allow_the_bet_to_time_out(self):
        """
        DESCRIPTION: In the Trader's Interface, allow the bet to time out
        EXPECTED: The bet should have timed out
        """
        pass

    def test_003_check_that_on_the_front_end_you_see_the_message_saying_that_the_bet_has_not_been_accepted_by_the_trader(self):
        """
        DESCRIPTION: Check that on the front end, you see the message saying that the bet has not been accepted by the Trader
        EXPECTED: You should see the message
        """
        pass

    def test_004_check_my_bets_open_bets_to_confirm_that_the_bet_has_not_been_placed(self):
        """
        DESCRIPTION: Check My Bets->Open Bets to confirm that the bet has not been placed
        EXPECTED: The bet should not have been placed
        """
        pass
