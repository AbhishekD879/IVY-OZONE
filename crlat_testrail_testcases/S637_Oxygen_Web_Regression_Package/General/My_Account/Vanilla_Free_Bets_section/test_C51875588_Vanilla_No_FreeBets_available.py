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
class Test_C51875588_Vanilla_No_FreeBets_available(Common):
    """
    TR_ID: C51875588
    NAME: [Vanilla] No FreeBets available
    DESCRIPTION: This test case verifies FreeBets menu item behaviour when there are no FreeBets available to the user
    PRECONDITIONS: - User has no FreeBets available
    """
    keep_browser_open = True

    def test_001_login_to_the_account_with_no_freebets_available(self):
        """
        DESCRIPTION: Login to the account with no FreeBets available
        EXPECTED: User is logged in
        """
        pass

    def test_002_coralnavigate_to_my_account__offers__free_bets__sports_free_betsladbrokesnavigate_to_my_account__promotions__free_betsornavigate_to_my_account__sports_free_bets(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Navigate to My Account > 'Offers & Free Bets' > Sports Free Bets
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Navigate to My Account > 'Promotions' > Free Bets
        DESCRIPTION: or
        DESCRIPTION: Navigate to My Account > Sports Free Bets
        EXPECTED: **Coral:**
        EXPECTED: * "MY FREE BETS/BONUSES" title (with the back button on the desktop)
        EXPECTED: * Total amount of Free Bets is displayed as "'free bets icon'<currency>0.00 Free Bets" text and the total balance of Free Bets displayed as "Total Balance: <currency>0.00"
        EXPECTED: **Ladbrokes:**
        EXPECTED: * "FREE BET" title (with the back button on the desktop)
        EXPECTED: * Total amount of Free Bets is displayed as "Free Bet Available (0)" text and the total balance of Free Bets displayed as "Total: <currency>0.00"
        """
        pass
