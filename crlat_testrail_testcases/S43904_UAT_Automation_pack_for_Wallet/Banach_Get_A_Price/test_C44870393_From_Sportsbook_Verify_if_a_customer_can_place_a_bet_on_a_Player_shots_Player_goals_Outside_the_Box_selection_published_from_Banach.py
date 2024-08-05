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
class Test_C44870393_From_Sportsbook_Verify_if_a_customer_can_place_a_bet_on_a_Player_shots_Player_goals_Outside_the_Box_selection_published_from_Banach(Common):
    """
    TR_ID: C44870393
    NAME: From Sportsbook, Verify if a customer can place a bet on a Player shots + Player goals Outside the Box selection published from Banach
    DESCRIPTION: Banach Bets on Player Shots and Player Goals Outside the Box Selection
    PRECONDITIONS: There should be Football matches for which Banach markets are available
    PRECONDITIONS: and  Player shots and Player goals Outside the Box selections are available.
    PRECONDITIONS: User should have balance to place bet.
    """
    keep_browser_open = True

    def test_001_load_app_and_navigate_to_any_football_landing_page(self):
        """
        DESCRIPTION: Load app and navigate to any Football Landing Page
        EXPECTED: Football Landing page is loaded with Matches tab open by default
        """
        pass

    def test_002_select_any_event_for_which_banach_markets_are_availablecoral__yourcallladbrokes__getaprice(self):
        """
        DESCRIPTION: Select any event for which Banach markets are available
        DESCRIPTION: Coral : #Yourcall
        DESCRIPTION: Ladbrokes : #GETAPRICE
        EXPECTED: Event landing page is loaded
        """
        pass

    def test_003_navigate_to_yourcall__getaprice_market_tab(self):
        """
        DESCRIPTION: Navigate to #Yourcall / #GETAPRICE market tab
        EXPECTED: #Yourcall / #GETAPRICE market tab is loaded
        """
        pass

    def test_004_add_player_shots__player_goals_outside_the_box_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add Player shots / Player goals Outside the Box selection to bet slip
        EXPECTED: Added selection should be shown on Quick bet / Betslip
        """
        pass

    def test_005_add_stake_and_place_bet(self):
        """
        DESCRIPTION: Add stake and Place bet
        EXPECTED: Bet should be placed successfully, and User should see the bat receipt.
        """
        pass
