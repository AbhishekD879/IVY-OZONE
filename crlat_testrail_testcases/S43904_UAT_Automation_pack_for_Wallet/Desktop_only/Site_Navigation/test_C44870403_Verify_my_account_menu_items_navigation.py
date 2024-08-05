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
class Test_C44870403_Verify_my_account_menu_items_navigation(Common):
    """
    TR_ID: C44870403
    NAME: Verify my account menu items navigation
    DESCRIPTION: Verify menu items available under My Account, user will be able to successfully navigate to these respective pages.
    PRECONDITIONS: User is logged in.
    """
    keep_browser_open = True

    def test_001_open_httpsbeta_sportscoralcouk_on_chrome_browser(self):
        """
        DESCRIPTION: Open https://beta-sports.coral.co.uk/ on Chrome browser.
        EXPECTED: https://beta-sports.coral.co.uk/ displayed on Chrome browser.
        """
        pass

    def test_002_click_on_login(self):
        """
        DESCRIPTION: Click on Login.
        EXPECTED: Login box appears.
        """
        pass

    def test_003_enter_username_and_password(self):
        """
        DESCRIPTION: Enter username and password.
        EXPECTED: User credentials displayed with password masked
        """
        pass

    def test_004_click_on_login(self):
        """
        DESCRIPTION: Click on Login.
        EXPECTED: User logged in successfully
        """
        pass

    def test_005_click_on_avatar_my_account(self):
        """
        DESCRIPTION: Click on Avatar (My Account)
        EXPECTED: Menu item links are available.
        """
        pass

    def test_006_verify_menu_item_links_availablebankingoffers__free_betshistorymessagesconnectsettingsgambling_controlshelp__contactlog_outdeposit(self):
        """
        DESCRIPTION: Verify menu item links available:
        DESCRIPTION: Banking
        DESCRIPTION: Offers & Free bets
        DESCRIPTION: History
        DESCRIPTION: Messages
        DESCRIPTION: Connect
        DESCRIPTION: Settings
        DESCRIPTION: Gambling Controls
        DESCRIPTION: Help & Contact
        DESCRIPTION: Log out
        DESCRIPTION: Deposit
        EXPECTED: Menu item links available:
        EXPECTED: Banking
        EXPECTED: Offers & Free bets
        EXPECTED: History
        EXPECTED: Messages
        EXPECTED: Connect
        EXPECTED: Settings
        EXPECTED: Gambling Controls
        EXPECTED: Help & Contact
        EXPECTED: Log out
        EXPECTED: Deposit
        """
        pass

    def test_007_navigate_to_banking(self):
        """
        DESCRIPTION: Navigate to Banking.
        EXPECTED: Banking page displayed:
        EXPECTED: My Balance
        EXPECTED: Deposit
        EXPECTED: Withdraw
        """
        pass

    def test_008_click_on_back__button(self):
        """
        DESCRIPTION: Click on back (<) button
        EXPECTED: Navigated back to Menu links
        """
        pass

    def test_009_click_on_history(self):
        """
        DESCRIPTION: Click on History.
        EXPECTED: Betting History
        EXPECTED: Transaction History
        EXPECTED: Payment History
        """
        pass

    def test_010_repeat_above_steps_for_all_menu_items_available(self):
        """
        DESCRIPTION: Repeat above steps for all menu items available.
        EXPECTED: Respective menu items display and user is able to navigate between them.
        """
        pass
