import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C61042783_Euro_Loyalty_Page_Customers_receives_a_badge_when_a_qualifying_bet_in_Betbuilder_is_placed_with_valid_stake_valid_odds(Common):
    """
    TR_ID: C61042783
    NAME: Euro Loyalty Page-Customers receives a badge when a qualifying bet  in Betbuilder is placed with valid stake & valid odds
    DESCRIPTION: This test case verifies whether a customer receives a badge when a qualifying bet is placed on a betbuilder with valid odds /stake
    PRECONDITIONS: Generic bet trigger should be  configured with min odds=1/2  stake=Â£5 to receive a badge
    """
    keep_browser_open = True

    def test_001_login_with_valid_user_credentials(self):
        """
        DESCRIPTION: Login with valid user credentials
        EXPECTED: User should be able to login into the application
        """
        pass

    def test_002_place_a_bet_with_stake_5_on_bet_builder_euro_game_with_odds_12(self):
        """
        DESCRIPTION: Place a bet with stake Â£5 on bet builder-Euro game with Odds =1/2
        EXPECTED: User should be able to place bet successfully
        """
        pass

    def test_003_navigate_to_euroloyaltyprogram_and_verify_that_the_user_receives_the_badge(self):
        """
        DESCRIPTION: Navigate to EuroLoyaltyProgram and verify that the user receives the badge.
        EXPECTED: User should receive the corresponding  badge
        EXPECTED: If the user is at freebet location, the user should be awarded with a badge and a freebet
        """
        pass
