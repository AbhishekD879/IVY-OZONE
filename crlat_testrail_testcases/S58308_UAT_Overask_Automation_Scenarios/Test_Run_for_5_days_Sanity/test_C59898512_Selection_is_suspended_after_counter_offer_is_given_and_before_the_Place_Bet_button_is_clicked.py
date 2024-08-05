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
class Test_C59898512_Selection_is_suspended_after_counter_offer_is_given_and_before_the_Place_Bet_button_is_clicked(Common):
    """
    TR_ID: C59898512
    NAME: Selection is suspended after counter offer is given and before the Place Bet button is clicked
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_make_a_selection_from_any_sportrace_and_try_and_place_a_bet_with_a_stake_greater_than_its_max_stake_so_that_overask_is_triggered(self):
        """
        DESCRIPTION: Make a selection from any sport/race and try and place a bet with a stake greater than its max stake so that Overask is triggered.
        EXPECTED: You should have tried to place a bet that triggers Overask and the bet should be in the Overask flow.
        """
        pass

    def test_002_make_any_type_of_counter_offer_in_ti(self):
        """
        DESCRIPTION: Make any type of counter offer in TI.
        EXPECTED: You should have given any type of counter offer and the counter offer should be seen on the front end.
        """
        pass

    def test_003_suspend_the_selection_in_openbetti(self):
        """
        DESCRIPTION: Suspend the selection in Openbet/TI.
        EXPECTED: The selection should be suspended and the counter offer on the front end should reflect this i.e. it should show the selection greyed out in the counter offer and a message should be seen
        """
        pass

    def test_004_verify_that_the_place_bet_button_is_not_clickable_and_that_you_cannot_place_the_bet(self):
        """
        DESCRIPTION: Verify that the Place Bet button is not clickable and that you cannot place the bet
        EXPECTED: The Place Bet button should not be clickable and you should not be able to place the bet
        """
        pass

    def test_005_click_on_the_cancel_button_and_verify_that_the_counter_offer_closes(self):
        """
        DESCRIPTION: Click on the Cancel button and verify that the counter offer closes.
        EXPECTED: The counter offer should close.
        """
        pass

    def test_006_check_my_bets_open_bets_to_make_sure_it_doesnt_show_that_the_bet_was_placed(self):
        """
        DESCRIPTION: Check My Bets->Open Bets to make sure it doesn't show that the bet was placed.
        EXPECTED: No bet should be showing in My Bets->Open Bets
        """
        pass
