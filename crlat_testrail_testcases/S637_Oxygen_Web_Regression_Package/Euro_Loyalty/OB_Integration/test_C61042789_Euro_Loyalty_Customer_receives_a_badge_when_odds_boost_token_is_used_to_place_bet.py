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
class Test_C61042789_Euro_Loyalty_Customer_receives_a_badge_when_odds_boost_token_is_used_to_place_bet(Common):
    """
    TR_ID: C61042789
    NAME: Euro Loyalty-Customer receives a badge when  odds boost token is used to place bet
    DESCRIPTION: This test case verifies whether a customer receives a badge  when a bet is placed using odds boost token
    PRECONDITIONS: Generic bet trigger should be  configured with min odds=1/2  stake=Â£5 to receive a badge
    """
    keep_browser_open = True

    def test_001_login_with_valid_user_credentials(self):
        """
        DESCRIPTION: Login with valid user credentials
        EXPECTED: User should be able to login into the application
        """
        pass

    def test_002_verify_if_the_customer_uses_odds_boost_token_to_boost_price_to_qualifying_odds_and_places_bet(self):
        """
        DESCRIPTION: Verify if the Customer uses odds boost token to boost price to qualifying odds and places bet
        EXPECTED: User should be able to place bet successfully with odds boost
        """
        pass

    def test_003_navigate_to_euroloyaltyprogram_and_verify_that_the_user_receives_the_badge(self):
        """
        DESCRIPTION: Navigate to EuroLoyaltyProgram and verify that the user receives the badge.
        EXPECTED: User should receive the corresponding  badge
        EXPECTED: If the user is at freebet location, the user should be awarded with a badge and a freebet
        """
        pass
