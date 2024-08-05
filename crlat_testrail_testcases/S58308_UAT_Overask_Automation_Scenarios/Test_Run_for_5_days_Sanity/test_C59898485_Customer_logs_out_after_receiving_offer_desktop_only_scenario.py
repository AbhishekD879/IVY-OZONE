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
class Test_C59898485_Customer_logs_out_after_receiving_offer_desktop_only_scenario(Common):
    """
    TR_ID: C59898485
    NAME: Customer logs out after receiving offer (desktop only scenario)
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_a_selection_to_bet_slip_and_trigger_overask(self):
        """
        DESCRIPTION: Add a selection to bet slip and trigger Overask
        EXPECTED: You bet should have gone to the Overask flow
        """
        pass

    def test_002_in_the_ti_give_any_type_of_counter_offer(self):
        """
        DESCRIPTION: In the TI, give any type of counter offer
        EXPECTED: You should have given a counter offer and should see the counter offer on the front end
        """
        pass

    def test_003_log_out_and_verify_that_you_do_not_see_the_counter_offer_anymore(self):
        """
        DESCRIPTION: Log out and verify that you do not see the counter offer anymore
        EXPECTED: You should not see the counter offer anymore and betslip should be cleared
        """
        pass

    def test_004_login_in_back_with_login_button_in_the_header(self):
        """
        DESCRIPTION: Login In back with Login button in the header.
        EXPECTED: User should see empty betslip
        """
        pass
