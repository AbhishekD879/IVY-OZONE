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
class Test_C51794967_Vanilla_Verify_FreeBets_navigation_Go_Betting(Common):
    """
    TR_ID: C51794967
    NAME: [Vanilla] Verify FreeBets navigation (‘Go Betting’)
    DESCRIPTION: This test case verifies "Go Betting" link on Sports Free Bets page
    PRECONDITIONS: - User has FreeBet(s) available
    PRECONDITIONS: - Instructions how to add freebet tokens for TEST2/STAGE users or existing PROD users with already granted tokens can be found here: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account (Select Reward Token = 2428)
    """
    keep_browser_open = True

    def test_001_login_to_the_account_with_freebets_available(self):
        """
        DESCRIPTION: Login to the account with FreeBet(s) available
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
        EXPECTED: Sports Free Bets is displayed
        """
        pass

    def test_003_coraltap_on_free_bet_cardnavigation_arrow__tap_on_bet_now_buttonladbrokestap_on_go_betting_link(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Tap on Free Bet Card/Navigation Arrow > Tap on 'Bet Now' button
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Tap on "Go Betting" link
        EXPECTED: - User is redirected to applicable event for the selected FreeBet
        EXPECTED: - When navigating to an event there should be an event id or other info in response present [to edit later on
        EXPECTED: according more specific parameter in a response]
        """
        pass
