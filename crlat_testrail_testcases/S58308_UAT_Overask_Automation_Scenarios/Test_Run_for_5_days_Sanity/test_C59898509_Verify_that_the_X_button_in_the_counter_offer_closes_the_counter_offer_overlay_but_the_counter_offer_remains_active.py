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
class Test_C59898509_Verify_that_the_X_button_in_the_counter_offer_closes_the_counter_offer_overlay_but_the_counter_offer_remains_active(Common):
    """
    TR_ID: C59898509
    NAME: Verify that the X button in the counter offer closes the counter offer overlay, but the counter offer remains active
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_make_a_bet_that_triggers_overask(self):
        """
        DESCRIPTION: Make a bet that triggers Overask
        EXPECTED: Your bet should have gone through to Overask
        """
        pass

    def test_002_make_any_type_of_counter_offer_in_the_ti(self):
        """
        DESCRIPTION: Make any type of counter offer in the TI
        EXPECTED: A counter offer should be seen on the counter offer
        """
        pass

    def test_003_click_on_the_x_in_the_top_left_hand_corner(self):
        """
        DESCRIPTION: Click on the X in the top left-hand corner.
        EXPECTED: The counter offer overlay should close.
        """
        pass

    def test_004_click_on_the_bet_slip_counter_in_the_top_right_hand_or_any_selection_should_open_the_overlay_and_show_that_your_counter_offer_is_still_active_provided_that_the_timer_has_not_run_out(self):
        """
        DESCRIPTION: Click on the bet slip counter in the top right-hand or any selection, should open the overlay and show that your counter offer is still active (provided that the timer has not run out)
        EXPECTED: The counter offer should still be active.
        """
        pass
