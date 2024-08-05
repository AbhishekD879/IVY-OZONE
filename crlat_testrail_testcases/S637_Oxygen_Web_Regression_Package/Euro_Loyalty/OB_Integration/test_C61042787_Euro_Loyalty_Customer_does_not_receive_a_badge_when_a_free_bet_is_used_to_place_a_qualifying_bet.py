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
class Test_C61042787_Euro_Loyalty_Customer_does_not_receive_a_badge_when_a_free_bet_is_used_to_place_a_qualifying_bet(Common):
    """
    TR_ID: C61042787
    NAME: Euro Loyalty-Customer does not receive a badge when a free bet is used to place a qualifying bet
    DESCRIPTION: This test case verifies whether a customer receives a badge  when a freebet  is used to place a qualifying bet
    PRECONDITIONS: Generic bet trigger should be configured with min odds=1/2  stake=Â£5 to receive a badge
    """
    keep_browser_open = True

    def test_001_login_with_valid_user_credentials(self):
        """
        DESCRIPTION: Login with valid user credentials
        EXPECTED: User should be able to login into the application
        """
        pass

    def test_002_verify_if_the__customer_places_a_qualifying_bet_using_a_freebet_received(self):
        """
        DESCRIPTION: Verify if the  Customer places a qualifying bet using a freebet received
        EXPECTED: User should be able to place bet successfully
        """
        pass

    def test_003_navigate_to_euroloyaltyprogram_and_verify_that_the_user_receives_the_badge(self):
        """
        DESCRIPTION: Navigate to EuroLoyaltyProgram and verify that the user receives the badge
        EXPECTED: User should not receive the corresponding badge
        """
        pass
