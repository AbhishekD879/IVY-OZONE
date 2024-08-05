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
class Test_C61042793_Euro_Loyalty_Received_Badge_Freebet_should_not_revert_if_we_do_cashout_befour_settlemet(Common):
    """
    TR_ID: C61042793
    NAME: Euro Loyalty-Received Badge/Freebet should not revert if we do cashout befour settlemet
    DESCRIPTION: This test case verifies whether a customer received badge/Freebet shuld not revert back if customer do cashout before settlement
    PRECONDITIONS: Generic bet trigger should be  configured with min odds=1/2  stake=Â£5 to receive a badge
    PRECONDITIONS: Config "Disable cash out check " Yes in OB offer
    """
    keep_browser_open = True

    def test_001_login_with_valid_user_credentials(self):
        """
        DESCRIPTION: Login with valid user credentials
        EXPECTED: User should be able to login into the application
        """
        pass

    def test_002_verify_if_the_customer_places_5_bet_at_12(self):
        """
        DESCRIPTION: Verify if the Customer places Â£5 bet at 1/2
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

    def test_004_cahout_the_bet_on_which_customer_got_badgefreebet(self):
        """
        DESCRIPTION: Cahout the bet on which customer got badge/freebet
        EXPECTED: Corresponding badge/freebet should not revert back.
        """
        pass
