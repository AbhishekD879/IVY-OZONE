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
class Test_C18011862_Verify_Free_Bets_listing_order(Common):
    """
    TR_ID: C18011862
    NAME: Verify Free Bets listing order
    DESCRIPTION: This test case verifies order in which Free Bets are listed
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User has more that 1 Free Bets with different expiration date available on his account
    """
    keep_browser_open = True

    def test_001_open_my_account_ladbrokes__right_menu_coral(self):
        """
        DESCRIPTION: Open My Account (Ladbrokes) / Right menu (Coral)
        EXPECTED: My Account / Right menu displayed
        """
        pass

    def test_002_coralclick_on_my_free_bets__bonuses_menu_itemladbrokesclick_on_free_bets_menu_item(self):
        """
        DESCRIPTION: *Coral*
        DESCRIPTION: Click on 'My Free Bets / Bonuses' menu item
        DESCRIPTION: *Ladbrokes*
        DESCRIPTION: Click on 'Free Bets' menu item
        EXPECTED: *Coral*
        EXPECTED: Free Bets page opened
        EXPECTED: *Ladbrokes*
        EXPECTED: Free Bets menu expanded
        """
        pass

    def test_003_verify_order_in_which_available_free_best_are_displayed(self):
        """
        DESCRIPTION: Verify order in which available Free Best are displayed
        EXPECTED: Free bets are listed in expiry date order
        EXPECTED: (if expiry date is the same, higher value bets are prioritized)
        """
        pass
