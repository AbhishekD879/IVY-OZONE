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
class Test_C61042784_Euro_Loyalty__Customers_receive_a_badge_when_two_qualifying_bets_are_placed_with_valid_stake_valid_odds_on_the_same_day(Common):
    """
    TR_ID: C61042784
    NAME: Euro Loyalty - Customers receive a badge when two qualifying bets are placed with valid stake & valid odds on the same day
    DESCRIPTION: This test case verifies  whether a customer  receives a badge upon placing 2 qualifying bets in the same day with valid odds/stake
    PRECONDITIONS: Generic bet trigger should be  configured with min odds=1/2  stake=Â£5 to receive a badge
    """
    keep_browser_open = True

    def test_001_login_with_valid_user_credentials(self):
        """
        DESCRIPTION: Login with valid user credentials
        EXPECTED: User should be able to login into the application
        """
        pass

    def test_002_places_2_qualifying_bets_on_the_same_day(self):
        """
        DESCRIPTION: places 2 qualifying bets on the same day
        EXPECTED: User should be able to place bet successfully
        """
        pass

    def test_003_navigate_to_euroloyaltyprogram_and_verify_that_the_user_receives_the_badge(self):
        """
        DESCRIPTION: Navigate to EuroLoyaltyProgram and verify that the user receives the badge.
        EXPECTED: User should receive only one badge
        EXPECTED: If the user is at freebet location, the user should be awarded with a badge and a freebet
        """
        pass
