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
class Test_C44870309_Verify_availability_bet_placement_and_bet_history_for_Private_market(Common):
    """
    TR_ID: C44870309
    NAME: Verify availability, bet placement and bet history for Private market.
    DESCRIPTION: 
    PRECONDITIONS: 1. User is assigned private market token in Open Bet.
    PRECONDITIONS: 2. User is logged in the application.
    """
    keep_browser_open = True

    def test_001_place_a_bet_with_the_following_conditions_1_the_selection_should_be_from_football___premier_league_competition2_the_oddsprice_value_should_be_greater_than_13_stake_should_be_1_while_placing_the_betafter_the_bet_is_placed_navigate_to_the_home_page_and_verify(self):
        """
        DESCRIPTION: Place a bet with the following conditions:-
        DESCRIPTION: 1. The selection should be from Football -> Premier League competition
        DESCRIPTION: 2. The odds/price value should be greater than 1.
        DESCRIPTION: 3. Stake should be £1 while placing the bet.
        DESCRIPTION: After the bet is placed, navigate to the Home page and verify.
        EXPECTED: A tab 'Enhanced Markets' id displayed besides the 'Highlights' tab/Home page.
        """
        pass

    def test_002_click_on_the_tab_enhanced_markets_verify(self):
        """
        DESCRIPTION: Click on the tab Enhanced Markets. Verify.
        EXPECTED: Private market for the user is displayed with selection name and odds/price.
        """
        pass

    def test_003_place_a_bet_on_the_private_market_and_verify(self):
        """
        DESCRIPTION: Place a bet on the private market and verify.
        EXPECTED: Bet on private market is placed successfully.
        """
        pass

    def test_004_navigate_to_my_bets_and_verify_in_open_bets(self):
        """
        DESCRIPTION: Navigate to My Bets and verify in Open Bets.
        EXPECTED: The bet placed on private market in step 3 is displayed.
        """
        pass
