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
class Test_C2983104_Verify_displaying_of_the_boosted_selections_in_the_My_Bets(Common):
    """
    TR_ID: C2983104
    NAME: Verify displaying of the boosted selections in the My Bets
    DESCRIPTION: 
    PRECONDITIONS: 1. Login as a user with a valid token added to some sport category
    PRECONDITIONS: 2. Place a bet on some boosted selection
    PRECONDITIONS: 3. Reuse this selection, place a bet without boosting
    PRECONDITIONS: 4. Go to My Bets > Open Bets
    """
    keep_browser_open = True

    def test_001_verify_the_this_bet_has_been_boosted_bar_and_the_appropriate_data_price_and_estimated_returns_are_shown_for_the_boosted_bet(self):
        """
        DESCRIPTION: Verify the "This bet has been boosted!" bar and the appropriate data: price and estimated returns are shown for the boosted bet
        EXPECTED: * The bar with Odds Boost icon and text "This bet has been boosted!" is located in the bottom of the bet
        EXPECTED: * Boosted odds are shown
        EXPECTED: * Boosted Estimated Returns are shown
        """
        pass

    def test_002_verify_the_this_bet_has_been_boosted_bar_isnt_shown_and_the_appropriate_price_and_estimated_returns_are_shown_for_the_not_boosted_bet(self):
        """
        DESCRIPTION: Verify the "This bet has been boosted!" bar isn't shown and the appropriate price and estimated returns are shown for the not-boosted bet
        EXPECTED: Non-boosted bet doesn't contains the bar. Not boosted odds and returns are shown
        """
        pass

    def test_003_pass_1_2_step_for_the_settled_bets_in_the_bet_history_tab(self):
        """
        DESCRIPTION: Pass 1-2 step for the settled bets in the Bet History tab
        EXPECTED: 
        """
        pass
