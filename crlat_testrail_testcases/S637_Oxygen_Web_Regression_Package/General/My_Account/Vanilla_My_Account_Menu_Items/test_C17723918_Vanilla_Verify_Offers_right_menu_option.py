import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C17723918_Vanilla_Verify_Offers_right_menu_option(Common):
    """
    TR_ID: C17723918
    NAME: [Vanilla] Verify Offers right menu option
    DESCRIPTION: This test case is to verify all option menus under Offers&Free bets right menu option
    PRECONDITIONS: User has account on QA env
    """
    keep_browser_open = True

    def test_001_log_in_to_test_env(self):
        """
        DESCRIPTION: Log in to test env
        EXPECTED: User is logged in, My Account button appears
        """
        pass

    def test_002_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap My Account button
        EXPECTED: Right menu is displayed
        """
        pass

    def test_003_clicktap_offersfree_bets_menu_option(self):
        """
        DESCRIPTION: Click/tap Offers&Free bets menu option
        EXPECTED: Offers&Free bets menu is displayed with the following options:
        EXPECTED: - Odds Boost
        EXPECTED: - Sports free bets
        EXPECTED: - Sports promotions
        EXPECTED: - Games promotions
        EXPECTED: - Voucher codes
        """
        pass

    def test_004_clicktap_odds_boost_option(self):
        """
        DESCRIPTION: Click/tap Odds Boost option
        EXPECTED: Odds boost page is displayed with the following information:
        EXPECTED: - Today's Odds Boost
        EXPECTED: - Boosts available now
        EXPECTED: - Upcoming boosts
        EXPECTED: - Terms and conditions
        """
        pass

    def test_005_reopen_right_menu__offersfree_bets_and_clicktap_sports_free_bets_option(self):
        """
        DESCRIPTION: Reopen right menu-> Offers&Free bets and click/tap Sports free bets option
        EXPECTED: User is taken to My freebets/bonuses page
        EXPECTED: Page contains the list of all freebets available to the user.
        """
        pass

    def test_006_reopen_right_menu__offersfree_bets_and_clicktap_sports_promotions_option(self):
        """
        DESCRIPTION: Reopen right menu-> Offers&Free bets and click/tap Sports promotions option
        EXPECTED: User is taken to My Promotions page with the list of all promotions available to the user
        """
        pass

    def test_007_reopen_right_menu__offersfree_bets_and_clicktap_games_promotions_option(self):
        """
        DESCRIPTION: Reopen right menu-> Offers&Free bets and click/tap Games promotions option
        EXPECTED: User is taken to My Offers page
        """
        pass

    def test_008_reopen_right_menu__offers_and_clicktap_voucher_codes_option(self):
        """
        DESCRIPTION: Reopen right menu-> Offers and click/tap Voucher codes option
        EXPECTED: User is taken to Redeem Voucher page
        """
        pass
