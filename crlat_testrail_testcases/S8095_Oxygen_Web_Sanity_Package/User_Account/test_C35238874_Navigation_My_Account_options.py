import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C35238874_Navigation_My_Account_options(Common):
    """
    TR_ID: C35238874
    NAME: Navigation 'My Account' options
    DESCRIPTION: Verify that "My Account" options open the correct page
    DESCRIPTION: AUTOMATED [C46032257]
    PRECONDITIONS: My Account Menu or User Menu is handled and set on GVC side.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_and_login(self):
        """
        DESCRIPTION: Load Oxygen app and login
        EXPECTED: * User is logged in successfully
        EXPECTED: * [My Account] button is displayed on Header with 'FB' icon available when user has freebets
        """
        pass

    def test_002_click_on_my_account_button_on_header(self):
        """
        DESCRIPTION: Click on [My Account] button on Header
        EXPECTED: Menu Overlay appears on full screen on Mobile and as a pop-up on Tablet/Desktop with next items ( configurable on GVC side):
        EXPECTED: * Banking
        EXPECTED: * Offers & Free Bets
        EXPECTED: * History
        EXPECTED: * Messages
        EXPECTED: * Connect
        EXPECTED: * Settings
        EXPECTED: * Gambling Controls
        EXPECTED: * Help & Contact
        EXPECTED: * Log Out
        EXPECTED: * Green'DEPOSIT' button
        EXPECTED: ![](index.php?/attachments/get/39072150)
        """
        pass

    def test_003__check_every_item_view(self):
        """
        DESCRIPTION: * Check every item view
        EXPECTED: * Every item has an icon an is left aligned
        EXPECTED: * 'Offers & Free Bets' have 'FB' icon if user has freebets
        EXPECTED: * 'Messages' have counter badge if user has rich inbox messages unread
        EXPECTED: * Arrow is present from right side for items that have further pop-up/overlay navigation ( e.g. Banking,Offers & Free Bets,History,Connect,Settings)
        """
        pass

    def test_004_click_on_banking_item(self):
        """
        DESCRIPTION: Click on 'Banking' item
        EXPECTED: Bankking Menu is opened with
        EXPECTED: * My balance
        EXPECTED: * Deposit
        EXPECTED: * Withdraw
        EXPECTED: ![](index.php?/attachments/get/13795464)
        """
        pass

    def test_005_click_my_balance_item_and_check_overlaypop_up_view(self):
        """
        DESCRIPTION: Click 'My balance' item and check Overlay/Pop-up view
        EXPECTED: My Balance Overlay/Pop-up is opened with next items:
        EXPECTED: * Withdrawable-online
        EXPECTED: * Restricted
        EXPECTED: * Available balance
        EXPECTED: * Total Balance
        EXPECTED: * Deposit Button
        EXPECTED: * Available to use on table
        EXPECTED: ![](index.php?/attachments/get/13967928)
        """
        pass

    def test_006_click_back__button_on_header_and_check_deposit_and_withdaw_item_navigation(self):
        """
        DESCRIPTION: Click back ('<') button on header and check 'Deposit' and 'Withdaw' item navigation
        EXPECTED: * Clicking on Deposit opens deposit Overlay/pop-up
        EXPECTED: * Clicking on Withdraw opens Withdraw Overlay
        """
        pass

    def test_007__go_back_and_open_my_account_menu_click_on_offers__free_bets(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Offers & Free Bets'
        EXPECTED: Offers Overlay is opened with next item menus:
        EXPECTED: * Odds Boost
        EXPECTED: * Sports Free Bets
        EXPECTED: * Sports Promotions
        EXPECTED: * Gaming Promotions
        EXPECTED: * Voucher Code
        EXPECTED: ![](index.php?/attachments/get/39224046)
        """
        pass

    def test_008_check_every_item_menu_navigation(self):
        """
        DESCRIPTION: Check every item menu navigation
        EXPECTED: * Odds Boost opens Odds Boost page
        EXPECTED: * Sports Free Bets opens Freebets page
        EXPECTED: * Sports Promotions opens Promotions page
        EXPECTED: * Gaming Promotions opens Gaming promotions ( external https://beta-promo.coral.co.uk/en/promo/offers)
        EXPECTED: * Voucher Code opens Voucher page ( https://beta-sports.coral.co.uk/voucher-code)
        """
        pass

    def test_009__go_back_and_open_my_account_menu_click_on_history(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'History'
        EXPECTED: History Overlay/pop-up is opened with next items:
        EXPECTED: * Betting History
        EXPECTED: * Transaction History
        EXPECTED: * Payment History
        EXPECTED: ![](index.php?/attachments/get/14054174)
        """
        pass

    def test_010_check_every_item_menu_navigation(self):
        """
        DESCRIPTION: Check every item menu navigation
        EXPECTED: * Betting History opens Settled Bets page/tab
        EXPECTED: * Transaction History opens Gaming history ( e.g. https://beta-sports.coral.co.uk/en/mobileportal/transactions)
        EXPECTED: * Payment History opens Payment history page ( e.g. https://cashier.coral.co.uk/home/txnSearchPageMerchant.action?sessionKey=198d8026e07f487fb348c516cc3d355a&LANG_ID=en&parent=https://beta-sports.coral.co.uk/)
        """
        pass

    def test_011__go_back_and_open_my_account_menu_click_on_messages(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Messages'
        EXPECTED: The Messages overlay/pop-up is opened with rich inbox messages available.
        """
        pass

    def test_012__go_back_and_open_my_account_menu_click_on_connect_the_grid_for_ladbrokes(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Connect' ('The Grid' for Ladbrokes)
        EXPECTED: 'Connect' Overlay/pop-up is opened with next items:
        EXPECTED: * Shop Exclusive Promos
        EXPECTED: * Shop Bet Tracker
        EXPECTED: * Football Bet Filter
        EXPECTED: * Shop Locator
        EXPECTED: ![](index.php?/attachments/get/14054175)
        EXPECTED: ![](index.php?/attachments/get/111161043)
        """
        pass

    def test_013_check_every_item_menu_navigation(self):
        """
        DESCRIPTION: Check every item menu navigation
        EXPECTED: * Shop Exclusive Promos opens Promotions page > Shop Exclusive tab
        EXPECTED: * Shop Bet Tracker opens Shop Bet Tracker page
        EXPECTED: * Football Bet Filter opens Football Bet Filter page
        EXPECTED: * Shop Locator opens Shop Locator page with map opened
        """
        pass

    def test_014__go_back_and_open_my_account_menu_click_on_settings(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Settings'
        EXPECTED: 'Settings'Overlay/pop-up is opened with next items:
        EXPECTED: * My Account Details
        EXPECTED: * Change Password
        EXPECTED: * Marketing Preferences
        EXPECTED: * Betting Setting
        EXPECTED: ![](index.php?/attachments/get/14054176)![](index.php?/attachments/get/111161044)
        """
        pass

    def test_015_check_every_item_menu_navigation(self):
        """
        DESCRIPTION: Check every item menu navigation
        EXPECTED: * My Account Details opens My account details overlay/pop-up
        EXPECTED: * Change Password opens Change Password overlay/pop-up
        EXPECTED: * Marketing Preferences opens  Communication Preferences
        EXPECTED: * Betting Setting opens Preferences Page
        """
        pass

    def test_016__go_back_and_open_my_account_menu_click_on_gambling_controls(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Gambling controls'
        EXPECTED: Gambling Controls Overlay/Pop-up is opened
        EXPECTED: ![](index.php?/attachments/get/14054187)
        """
        pass

    def test_017__go_back_and_open_my_account_menu_click_on_help__contact(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Help & Contact'
        EXPECTED: 'Help & Contact' Overlay/Pop-up is opened
        EXPECTED: ![](index.php?/attachments/get/14054189)
        """
        pass

    def test_018__go_back_and_open_my_account_menu_click_on_log_out(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Log Out'
        EXPECTED: User is logged out
        """
        pass
