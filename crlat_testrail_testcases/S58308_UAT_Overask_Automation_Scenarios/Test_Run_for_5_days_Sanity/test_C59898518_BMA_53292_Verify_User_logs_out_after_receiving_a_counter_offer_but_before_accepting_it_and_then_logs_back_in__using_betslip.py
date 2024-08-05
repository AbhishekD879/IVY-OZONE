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
class Test_C59898518_BMA_53292_Verify_User_logs_out_after_receiving_a_counter_offer_but_before_accepting_it_and_then_logs_back_in__using_betslip(Common):
    """
    TR_ID: C59898518
    NAME: BMA-53292: Verify User logs out after receiving a counter offer but before accepting it and then logs back in - using betslip
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_1_log_in(self):
        """
        DESCRIPTION: 1. Log in
        EXPECTED: User should be logged in
        """
        pass

    def test_002_place_an_oa_bet_using_betslip(self):
        """
        DESCRIPTION: Place an OA bet using betslip
        EXPECTED: Bet should have gone through to OA and trader should see it in TI.
        """
        pass

    def test_003_when_the_counter_offer_is_received_log_out_of_the_application(self):
        """
        DESCRIPTION: When the counter offer is received, log out of the application
        EXPECTED: The user should be logged out
        """
        pass

    def test_004_verify_that_the_betslip_has_been_cleared(self):
        """
        DESCRIPTION: Verify that the betslip has been cleared
        EXPECTED: The betslip should have been cleared
        """
        pass

    def test_005_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: The user should be logged in
        """
        pass

    def test_006_verify_that_betslip_is_empty_ie_you_should_not_see_the_counter_offer_and_you_should_not_see_any_selections(self):
        """
        DESCRIPTION: Verify that betslip is empty i.e. you should not see the counter offer and you should not see any selections
        EXPECTED: No counter offer or selection should be seen in the betslip
        """
        pass
