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
class Test_C61042781_Euro_Loyalty_Page_Customers_not_receives_a_badge_when_a_qualifying_bet_is_placed_with_invalid_stake_valid_odds(Common):
    """
    TR_ID: C61042781
    NAME: Euro Loyalty Page- Customers not receives a badge when a qualifying bet is placed with invalid stake & valid odds
    DESCRIPTION: This test case verifies whether a customer receives a badge when a qualifying bet is placed with invalid stake& valid odds
    PRECONDITIONS: Generic bet trigger should be  configured with min odds=1/2  stake=Â£5 to receive a badge
    """
    keep_browser_open = True

    def test_001_login_with_valid_user_credentials(self):
        """
        DESCRIPTION: Login with valid user credentials
        EXPECTED: User should be able to login into the application
        """
        pass

    def test_002_place_a_bet_with_stake_4_on_a_bet_with_odds_12(self):
        """
        DESCRIPTION: Place a bet with stake Â£4 on a bet with Odds =1/2
        EXPECTED: User should be able to place bet successfully
        """
        pass

    def test_003_navigate_to_euroloyaltyprogram_and_verify_that_the_user_receives_the_badge(self):
        """
        DESCRIPTION: Navigate to EuroLoyaltyProgram and verify that the user receives the badge
        EXPECTED: User should not receive any badge
        """
        pass
