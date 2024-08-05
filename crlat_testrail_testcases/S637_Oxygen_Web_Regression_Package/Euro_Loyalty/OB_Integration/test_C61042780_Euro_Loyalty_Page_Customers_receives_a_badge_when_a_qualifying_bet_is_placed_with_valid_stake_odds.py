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
class Test_C61042780_Euro_Loyalty_Page_Customers_receives_a_badge_when_a_qualifying_bet_is_placed_with_valid_stake_odds(Common):
    """
    TR_ID: C61042780
    NAME: Euro Loyalty Page- Customers receives a badge when a qualifying bet is placed with valid stake/odds
    DESCRIPTION: This test case verifies whether a customer receives a badge when a qualifying bet is placed with valid stake/odds
    PRECONDITIONS: Generic bet trigger should be  configured with min odds=1/2  stake=Â£5 to receive a badge
    """
    keep_browser_open = True

    def test_001_login_with_valid_user_credentials(self):
        """
        DESCRIPTION: Login with valid user credentials
        EXPECTED: User should be able to login into the application
        """
        pass

    def test_002_place_a_bet_with_stake_5_on_a_bet_with_odds_12(self):
        """
        DESCRIPTION: Place a bet with stake Â£5 on a bet with Odds =1/2
        EXPECTED: User should be able to place bet successfully
        """
        pass

    def test_003_navigate_to_euroloyaltyprogram_and_verify_that_the_user_receives_the_badge_upon_satisfying_the_above_conditions(self):
        """
        DESCRIPTION: Navigate to EuroLoyaltyProgram and verify that the user receives the badge upon satisfying the above conditions
        EXPECTED: User should receive the corresponding  badge
        EXPECTED: If the user is at freebet location, the user should be awarded with a badge and a freebet
        """
        pass
