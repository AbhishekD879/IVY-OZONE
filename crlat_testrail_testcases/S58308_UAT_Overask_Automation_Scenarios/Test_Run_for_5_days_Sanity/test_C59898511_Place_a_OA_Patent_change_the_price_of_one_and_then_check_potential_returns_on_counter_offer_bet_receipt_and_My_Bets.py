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
class Test_C59898511_Place_a_OA_Patent_change_the_price_of_one_and_then_check_potential_returns_on_counter_offer_bet_receipt_and_My_Bets(Common):
    """
    TR_ID: C59898511
    NAME: Place a OA Patent, change the price of one and then check potential returns on counter offer, bet receipt and My Bets
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_a_patent_bet_that_triggers_overask(self):
        """
        DESCRIPTION: Place a Patent bet that triggers Overask
        EXPECTED: You should have placed a Patent bet that goes through to the Overask flow
        """
        pass

    def test_002_in_ti_counter_offer_by_changing_the_price_of_one_of_the_selections(self):
        """
        DESCRIPTION: In TI, counter offer by changing the price of one of the selections.
        EXPECTED: You should have counter offered by changing the price of one selections.
        """
        pass

    def test_003_in_the_counter_offer_verify_that_the_new_price_is_highlighted_in_yellow_for_the_selection_and_the_old_price_should_be_shown_with_a_strike_through(self):
        """
        DESCRIPTION: In the counter offer, verify that the new price is highlighted in yellow for the selection and the old price should be shown with a strike through.
        EXPECTED: The new price should be highlighted in yellow and the old price should be struck through.
        """
        pass

    def test_004_verify_that_the_new_potential_returns_are_correct_ie_they_are_calculated_using_the_new_price(self):
        """
        DESCRIPTION: Verify that the new potential returns are correct i.e. they are calculated using the new price
        EXPECTED: The new potential returns should be correct.
        """
        pass

    def test_005_place_the_bet_and_verify_that_the_bet_receipt_also_shows_the_correct_new_potential_returns(self):
        """
        DESCRIPTION: Place the bet and verify that the bet receipt also shows the correct new potential returns.
        EXPECTED: The bet receipt should show the correct new potential returns.
        """
        pass

    def test_006_go_to_my_bets_open_bets_and_verify_that_the_new_potential_returns_are_correct_and_the_selection_for_which_you_changed_the_price_shows_the_new_price(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and verify that the new potential returns are correct and the selection for which you changed the price shows the new price.
        EXPECTED: My Bets->Open Bets should show the new price and the correct new potential returns
        """
        pass
