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
class Test_C61042785_Euro_Loyalty_Customers_receive_a_badge_when_a_new_qualifying_bet_is_added_to_bet_slip_but_not_placed_until_000001_next_day_where_the_customer_is_already_awarded_with_daily_badge(Common):
    """
    TR_ID: C61042785
    NAME: Euro Loyalty -Customers receive a badge when a new qualifying bet is  added to bet slip but not placed until 00:00:01 (next day), where the customer is already awarded with daily badge
    DESCRIPTION: This test case verifies  whether a customer  receives a badge when a new qualifying bet is  added to bet slip but not placed until 00:00:01 (next day), where the customer is already awarded with daily badge
    PRECONDITIONS: Generic bet trigger should be  configured with min odds=1/2  stake=Â£5 to receive a badge
    """
    keep_browser_open = True

    def test_001_login_with_valid_user_credentials(self):
        """
        DESCRIPTION: Login with valid user credentials
        EXPECTED: User should be able to login into the application
        """
        pass

    def test_002_place_a_qualified_bet(self):
        """
        DESCRIPTION: place a qualified bet
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

    def test_004_add_a_qualified_selection_to_betslip_and_place_be__000001_bst_next_day(self):
        """
        DESCRIPTION: Add a qualified selection to betslip and place be @ 00:00:01 BST (next day)
        EXPECTED: User should be able to place bet successfully
        """
        pass

    def test_005_navigate_to_euroloyaltyprogram_and_verify_that_the_user_receives_the_badge(self):
        """
        DESCRIPTION: Navigate to EuroLoyaltyProgram and verify that the user receives the badge.
        EXPECTED: User should receive the corresponding  badge
        EXPECTED: If the user is at freebet location, the user should be awarded with a badge and a freebet
        """
        pass
