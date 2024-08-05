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
class Test_C61042794_Euro_Loyalty_Customer_receives_a_badge_when_a_bet_is_placed_on_an_upcoming_Euro_match(Common):
    """
    TR_ID: C61042794
    NAME: Euro Loyalty-Customer receives a badge when a bet is placed on an upcoming Euro match
    DESCRIPTION: This test case verifies whether a customer receives a badge when a bet is placed on an upcoming euro match
    PRECONDITIONS: Generic bet trigger should be  configured with min odds=1/2  stake=Â£5 to receive a badge
    """
    keep_browser_open = True

    def test_001_login_with_valid_user_credentials(self):
        """
        DESCRIPTION: Login with valid user credentials
        EXPECTED: User should be able to login into the application
        """
        pass

    def test_002_verify_if_the_customer_places_qualifying_bet_in_the_days_leading_up_to_the_euros(self):
        """
        DESCRIPTION: Verify if the Customer places qualifying bet in the days leading up to the Euros
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