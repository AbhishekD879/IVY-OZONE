import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C51702947_Vanilla_Ladbrokes_Verify_FreeBets_displaying_in_my_Account(Common):
    """
    TR_ID: C51702947
    NAME: [Vanilla Ladbrokes] Verify FreeBets displaying in my Account.
    DESCRIPTION: This test case verifies that users are able to see what FreeBets they have available.
    PRECONDITIONS: - User is logged in with only 1 FreeBet available
    PRECONDITIONS: - Instructions how to add freebet tokens for TEST2/STAGE users or existing PROD users with already granted tokens can be found here: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account (Select Reward Token = 2428)
    """
    keep_browser_open = True

    def test_001_navigate_to_my_account_gt_promotions_gt_free_betsornavigate_to_my_account_gt_sports_free_bets(self):
        """
        DESCRIPTION: Navigate to My Account &gt; 'Promotions' &gt; Free Bets
        DESCRIPTION: or
        DESCRIPTION: Navigate to My Account &gt; Sports Free Bets
        EXPECTED: Sports Free Bets page is displayed
        """
        pass

    def test_002_validate_sports_free_bets_page(self):
        """
        DESCRIPTION: Validate Sports Free Bets page
        EXPECTED: - "FREE BET" title (with the back button on the desktop)
        EXPECTED: - Total amount of Free Bets is displayed next to "Free Bet Available" text and total balance of Free Bets (sum of the existing ones) displayed as "Total: 'amount: currency sum'"
        EXPECTED: - List of available free bets.
        """
        pass

    def test_003_check_elements_of_available_free_bet(self):
        """
        DESCRIPTION: Check elements of available free bet
        EXPECTED: - FreeBet amount
        EXPECTED: - Use by date (e.g. DD/MM/YYYY - HH:MM)
        EXPECTED: - Text taken from ‘freebetOfferName’ (e.g. “Acca Insurance”, “Money back”)
        EXPECTED: - Go Betting link
        EXPECTED: - "i" information icon
        """
        pass

    def test_004_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out
        """
        pass

    def test_005_login_to_the_account_with_multiple_freebets_available_and_validate__list_using_the_next_steps_1_3(self):
        """
        DESCRIPTION: Login to the account with multiple FreeBets available and validate  list using the next steps (1-3)
        EXPECTED: - All available FreeBets are displayed sorted by expiration date (Use By)
        """
        pass
