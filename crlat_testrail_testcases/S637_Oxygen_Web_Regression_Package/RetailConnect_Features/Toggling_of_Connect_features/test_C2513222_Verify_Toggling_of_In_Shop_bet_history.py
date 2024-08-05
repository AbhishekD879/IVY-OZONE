import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2513222_Verify_Toggling_of_In_Shop_bet_history(Common):
    """
    TR_ID: C2513222
    NAME: Verify Toggling of 'In-Shop bet history'
    DESCRIPTION: This test case verify that In-Shop Bet History can be switched on/off in CMS:
    DESCRIPTION: CMS -> System configuration -> Connect -> shop Bet History
    PRECONDITIONS: 1. Load CMS and make sureIn-Shop Bet History is turned off: System configuration -> Connect -> shop Bet History = false (the rest of Connect features are turned on)
    PRECONDITIONS: 2. Load SportBook App
    PRECONDITIONS: 3. Log in
    """
    keep_browser_open = True

    def test_001__tap_my_bet_verify_presence_of_in_shop_bets_tab(self):
        """
        DESCRIPTION: * Tap 'My Bet'
        DESCRIPTION: * Verify presence of 'In-Shop Bets' tab
        EXPECTED: * 'My Bets' page is opened
        EXPECTED: * There is no In-Shop Bets' tab
        """
        pass

    def test_002_try_to_navigate_to_in_shop_bets_tab_by_direct_linkhttpscoralcoukin_shop_bets(self):
        """
        DESCRIPTION: Try to navigate to 'In-Shop Bets' tab by direct link
        DESCRIPTION: https://***.coral.co.uk/in-shop-bets
        EXPECTED: Home page is opened instead
        """
        pass

    def test_003__load_cms_turn_shop_bet_history_feature_on_reload_sportbook_app(self):
        """
        DESCRIPTION: * Load CMS
        DESCRIPTION: * Turn 'shop Bet History' feature on
        DESCRIPTION: * Reload SportBook App
        EXPECTED: 
        """
        pass

    def test_004__tap_my_bet_verify_presence_of_in_shop_bets_tab(self):
        """
        DESCRIPTION: * Tap 'My Bet'
        DESCRIPTION: * Verify presence of 'In-Shop Bets' tab
        EXPECTED: * 'My Bets' page is opened
        EXPECTED: * Tab 'In-Shop Bets' is displayed (the last one)
        """
        pass

    def test_005_open_in_shop_bets_tab(self):
        """
        DESCRIPTION: Open 'In-Shop Bets' tab
        EXPECTED: * 'In-Shop Bets' tab is opened
        EXPECTED: * It shows 'i' icon and 'You have no In-Shop bet history.'
        """
        pass
