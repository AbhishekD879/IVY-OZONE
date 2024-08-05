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
class Test_C44870294_2_singles_1_with_OA_and_another_without_OA_and_trader_times_out(Common):
    """
    TR_ID: C44870294
    NAME: 2 singles : 1 with OA and another without OA and trader times out
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_one_oa_bet_and_one_non_oa_bet(self):
        """
        DESCRIPTION: Place one OA bet and one non-OA bet
        EXPECTED: The bets should have gone through to the OA flow
        """
        pass

    def test_002_in_the_ti_allow_the_oa_bet_to_time_out(self):
        """
        DESCRIPTION: In the TI, allow the OA bet to time out
        EXPECTED: The bet should have timed out
        """
        pass

    def test_003_check_that_you_see_the_message_that_the_bets_have_not_been_accepted_by_traders(self):
        """
        DESCRIPTION: Check that you see the message that the bets have not been accepted by Traders
        EXPECTED: You should see the message and the bets should not have been placed
        """
        pass
