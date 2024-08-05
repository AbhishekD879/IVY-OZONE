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
class Test_C62255356_Verify_display_of_Free_Bets_for_Bet_Pack_in_my_Account(Common):
    """
    TR_ID: C62255356
    NAME: Verify display of Free Bets for Bet Pack in my Account.
    DESCRIPTION: This test case verifies display of Free Bets for Bet Pack in my Account.
    PRECONDITIONS: 1: Bet Pack should be Purchased and Congratulations page should be displayed to the user
    PRECONDITIONS: 2: Login to Application
    """
    keep_browser_open = True

    def test_001_navigate_to_my_account__sports_free_bets(self):
        """
        DESCRIPTION: Navigate to My Account > Sports Free Bets
        EXPECTED: Sports Free Bets page should be displayed
        """
        pass

    def test_002_validate_sports_free_bets_page(self):
        """
        DESCRIPTION: Validate Sports Free Bets page
        EXPECTED: List of Free Bets for Bet Pack should be displayed
        """
        pass

    def test_003_check_elements_of_free_bet(self):
        """
        DESCRIPTION: Check elements of free bet
        EXPECTED: - FreeBet amount
        EXPECTED: - Use by date (e.g. DD/MM/YYYY - HH:MM)
        EXPECTED: - Text taken from ‘freebetOfferName’ (e.g. “Acca Insurance”, “Money back”)
        EXPECTED: - Go Betting link
        EXPECTED: - "i" information icon
        """
        pass
