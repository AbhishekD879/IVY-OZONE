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
class Test_C59898517_BMA_53292_Verify_User_logs_out_after_receiving_a_counter_offer_but_before_accepting_it_using_the_betslip(Common):
    """
    TR_ID: C59898517
    NAME: BMA-53292: Verify User logs out after receiving a counter offer but before accepting it using the betslip
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User should be logged in
        """
        pass

    def test_002_place_an_oa_bet_using_betslip(self):
        """
        DESCRIPTION: Place an OA bet using betslip
        EXPECTED: Bet should have gone through to OA and trader should see it in TI.
        """
        pass

    def test_003_trader_should_give_a_counter_offer(self):
        """
        DESCRIPTION: Trader should give a counter offer
        EXPECTED: Counter offer should be seen on FE
        """
        pass

    def test_004_when_the_counter_offer_is_received_log_out_of_the_application(self):
        """
        DESCRIPTION: When the counter offer is received, log out of the application
        EXPECTED: User should be logged out
        """
        pass

    def test_005_verify_that_the_betslip_has_been_cleared(self):
        """
        DESCRIPTION: Verify that the betslip has been cleared
        EXPECTED: No counter offer or selection should be seen in the betslip
        """
        pass
