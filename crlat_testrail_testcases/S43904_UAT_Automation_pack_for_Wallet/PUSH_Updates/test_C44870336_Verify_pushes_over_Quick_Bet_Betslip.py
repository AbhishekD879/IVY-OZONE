import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870336_Verify_pushes_over_Quick_Bet_Betslip(Common):
    """
    TR_ID: C44870336
    NAME: Verify pushes over Quick Bet/ Betslip
    DESCRIPTION: Verify pushes over Quick Bet/ Betslip
    PRECONDITIONS: User loads the https://beta-sports.coral.co.uk/ and logs in.
    PRECONDITIONS: User make one or more selections
    """
    keep_browser_open = True

    def test_001_user_make_a_selection_and_verify_that_the_selection_is_added_to_quick_bet_betslipand_stake_is_entered(self):
        """
        DESCRIPTION: User make a selection and verify that the selection is added to Quick Bet/ Betslip
        DESCRIPTION: And stake is entered
        EXPECTED: The selection is added to Quick Bet/ Betslip
        EXPECTED: entered
        """
        pass

    def test_002_verify_that_when_a_push_happens_due_to_odds_changes_this_is_reflected_in_quick_bet_betslip__user_is_displayed_the_right_message__the_odds_are_changed_to_the_new_value__the_potential_returns_are_reflecting_the_new_value(self):
        """
        DESCRIPTION: Verify that when a push happens due to odds changes, this is reflected in Quick Bet/ Betslip:
        DESCRIPTION: - user is displayed the right message
        DESCRIPTION: - the odds are changed to the new value
        DESCRIPTION: - the potential returns are reflecting the new value
        EXPECTED: When a push ( odds values changes) happens, this is reflected in Quick Bet/ Betslip
        """
        pass

    def test_003_verify_that_when_a_push_due_to_suspended_selectionsmarketsevents_or_na_markets_happens_this_is_reflected_in_quick_bet_betslip__user_is_displayed_the_right_message__the_place_a_bet_button_is_grayed_out_and_not_clickableverify_that_if_selectionsmarketsevents_are_becoming_available_this_is_reflected_in_quick_betbetslip(self):
        """
        DESCRIPTION: Verify that when a push due to suspended selections/markets/events or NA markets happens, this is reflected in Quick Bet/ Betslip:
        DESCRIPTION: - user is displayed the right message
        DESCRIPTION: - the 'place a bet' button is grayed out and not clickable
        DESCRIPTION: Verify that if selections/markets/events are becoming available, this is reflected in Quick Bet/Betslip
        EXPECTED: When a push (suspended, NA) happens, this is reflected in Quick Bet/ Betslip
        """
        pass
