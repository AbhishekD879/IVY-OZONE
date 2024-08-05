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
class Test_C59898489_Customer_with_an_odds_boost_token_tries_to_place_a_bet_using_the_token_and_a_stake_which_is_both_greater_than_the_max_stake_for_a_selection_and_max_stake_for_the_odds_boost(Common):
    """
    TR_ID: C59898489
    NAME: Customer with an odds boost token tries to place a bet using the token and a stake which is both greater than the max stake for a selection and max stake for the odds boost
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_a_selection_to_bet_slip_or_quick_bet_click_on_the_odds_boost_button_and_add_a_stake_which_is_greater_than_both_the_max_stake_for_the_selection_and_the_max_stake_allowed_for_odds_boost(self):
        """
        DESCRIPTION: Add a selection to bet slip or Quick Bet, click on the Odds Boost button and add a stake which is greater than both the max stake for the selection and the max stake allowed for Odds Boost.
        EXPECTED: Customer should see a pop up telling them the max stake associated with the Odds Boost token and they should not be able to place the bet. They should be able to change their stake and try to place a bet again.
        """
        pass
