import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C44870243_Verify_partial_cash_out_button_with_the_potential_returns_amount_on_the_cash_out__Open_Bets_tab_Verify_the_partial_cash_out_button_and_also_the_slider_with_proposed_cash_out_values_default_position_of_slider_in_middle_as_per_production__Verify(Common):
    """
    TR_ID: C44870243
    NAME: Verify partial cash-out button with the potential returns amount on the cash-out  /Open Bets tab -Verify the partial cash-out button and also the slider with proposed cash out values (default position of slider in middle as per production) - Verify
    DESCRIPTION: "-Verify partial cash-out button with the potential returns amount on the cash-out  /Open Bets tab
    DESCRIPTION: -Verify the partial cash-out button and also the slider with proposed cash out values (default position of slider in middle as per production)
    DESCRIPTION: - Verify by adjusting the slider up or down and the partial cashout value changes absed on slider .
    DESCRIPTION: "
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_a_single_on_a_cash_out_market(self):
        """
        DESCRIPTION: Place a single on a Cash Out market
        EXPECTED: You should have placed a single
        """
        pass

    def test_002_go_to_my_bets_open_bets_and_verify_that_your_bet_has_partial_cash_out_available_if_it_does_not_place_more_single_bets_until_you_have_a_bet_with_partial_cash_out(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and verify that your bet has Partial Cash Out available. (If it does not, place more single bets until you have a bet with partial cash out)
        EXPECTED: Your bet should have Partial Cash Out available.
        """
        pass

    def test_003_click_on_the_partial_cash_out_button_and_verify_the_slider_with_proposed_cash_out_values_default_position_of_slider_in_middle_as_per_production(self):
        """
        DESCRIPTION: Click on the Partial Cash Out button and verify the slider with proposed cash out values (default position of slider in middle as per production)
        EXPECTED: You should see the slider with proposed cash out values (default position of slider in middle as per production)
        """
        pass

    def test_004_verify_that_sliding_to_the_left_decreases_you_cash_out_value_and_sliding_to_the_right_increases_it(self):
        """
        DESCRIPTION: Verify that sliding to the left decreases you cash out value and sliding to the right increases it
        EXPECTED: Sliding to the left should decrease the cash out value and sliding to the right should increase it
        """
        pass

    def test_005_verify_that_clicking_on_the_x_closes_partial_cash_out_slider(self):
        """
        DESCRIPTION: Verify that clicking on the X closes Partial Cash Out slider
        EXPECTED: Clicking on the X should close Partial Cash Out slider
        """
        pass

    def test_006_verify_that_clicking_on_the_cash_out_value_shows_you_the_confirm_cash_out_button_which_when_clicked_partially_cashes_out_the_bet(self):
        """
        DESCRIPTION: Verify that clicking on the Cash Out Value shows you the Confirm Cash Out button which when clicked partially cashes out the bet
        EXPECTED: You should see the Confirm Cash Out Button and clicking it should partially cash out your bet
        """
        pass
