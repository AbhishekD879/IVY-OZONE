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
class Test_C59482943_Verify_navigation_of_My_Account_options(Common):
    """
    TR_ID: C59482943
    NAME: Verify navigation of  'My Account' options
    DESCRIPTION: This test case verifies opening the correct pages by clicking/tapping on 'My Account' options.
    DESCRIPTION: **Note:**
    DESCRIPTION: My Account Menu or User Menu is handled and set on GVC side.
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Log in with valid credentials
    PRECONDITIONS: 3. Make sure that the 'My Account' button is displayed on Header with 'FB' icon available when the user has free bets
    PRECONDITIONS: 4. Click/Tap the 'My Account' button on the Header
    PRECONDITIONS: 5. Make sure that 'My Account' is opened and contains the following items:
    PRECONDITIONS: **Coral**
    PRECONDITIONS: * 'Menu' title and 'Close' button
    PRECONDITIONS: * Banking
    PRECONDITIONS: * Offers & Free Bets
    PRECONDITIONS: * History
    PRECONDITIONS: * Messages
    PRECONDITIONS: * Connect
    PRECONDITIONS: * Settings
    PRECONDITIONS: * Gambling Controls
    PRECONDITIONS: * Help & Contact
    PRECONDITIONS: * Log Out
    PRECONDITIONS: * Green'DEPOSIT' button
    PRECONDITIONS: **Ladbrokes**
    PRECONDITIONS: * 'Menu' title and 'Close' button
    PRECONDITIONS: * Banking & Balances
    PRECONDITIONS: * Promotions
    PRECONDITIONS: * Odds Boosts
    PRECONDITIONS: * Sports Free Bets
    PRECONDITIONS: * My Bets
    PRECONDITIONS: * Messages
    PRECONDITIONS: * History
    PRECONDITIONS: * The Grid
    PRECONDITIONS: * Settings
    PRECONDITIONS: * Gambling Controls
    PRECONDITIONS: * Help & Contact
    PRECONDITIONS: * Log Out
    PRECONDITIONS: * Green'DEPOSIT' button
    """
    keep_browser_open = True

    def test_001_clicktap_on_bankingbanking__balances_item(self):
        """
        DESCRIPTION: Click/Tap on 'Banking'/'Banking & Balances' item
        EXPECTED: 'Banking'/'Banking & Balances' Menu is opened with the following items:
        EXPECTED: **Coral**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * My balance
        EXPECTED: * Deposit
        EXPECTED: * Withdraw
        EXPECTED: ![](index.php?/attachments/get/115420271)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * My balance
        EXPECTED: * Deposit
        EXPECTED: * Transfer
        EXPECTED: * Withdraw
        EXPECTED: * Payment History
        EXPECTED: ![](index.php?/attachments/get/115420277)
        """
        pass

    def test_002_clicktap_my_balance_item_and_verify_overlaypop_up_view(self):
        """
        DESCRIPTION: Click/Tap 'My balance' item and verify Overlay/Pop-up view
        EXPECTED: 'My Balance' Overlay/Pop-up is opened with the following items:
        EXPECTED: **Coral**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Withdrawable-online
        EXPECTED: * Restricted
        EXPECTED: * Available balance
        EXPECTED: * Total Balance
        EXPECTED: * Deposit Button
        EXPECTED: * 'Available to use on' table
        EXPECTED: ![](index.php?/attachments/get/115420294)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Withdrawable-online
        EXPECTED: * Available balance
        EXPECTED: * Total Balance
        EXPECTED: * Deposit Button
        EXPECTED: * 'Available to use on' table
        EXPECTED: ![](index.php?/attachments/get/115420297)
        """
        pass

    def test_003_clicktap_back__button_on_header_and_check_deposit_and_withdraw_item_navigation(self):
        """
        DESCRIPTION: Click/Tap 'Back' ('<') button on header and check 'Deposit' and 'Withdraw' item navigation
        EXPECTED: * Clicking on Deposit opens deposit Overlay/pop-up
        EXPECTED: * Clicking on Withdraw opens Withdraw Overlay
        """
        pass

    def test_004__go_back_and_open_my_account_menu_clicktap_on_offers__free_betspromotions_item(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Offers & Free Bets'/'Promotions' item
        EXPECTED: 'Offers'/'Promotions' Overlay/Pop-up is opened with the following items:
        EXPECTED: **Coral**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Odds Boost
        EXPECTED: * Sports Free Bets
        EXPECTED: * Sports Promotions
        EXPECTED: * Gaming Promotions
        EXPECTED: * Voucher Code
        EXPECTED: ![](index.php?/attachments/get/39224046)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Free Bets
        EXPECTED: * Odds Boost
        EXPECTED: * Sports Promotions
        EXPECTED: * Gaming Promotions
        EXPECTED: ![](index.php?/attachments/get/115421347)
        """
        pass

    def test_005_verify_every_item_menu_navigation_by_clickingtapping_on_it(self):
        """
        DESCRIPTION: Verify every item menu navigation by clicking/tapping on it
        EXPECTED: **Coral**
        EXPECTED: * Odds Boost opens Odds Boost page
        EXPECTED: * Sports Free Bets opens Freebets page
        EXPECTED: * Sports Promotions opens Promotions page
        EXPECTED: * Gaming Promotions opens Gaming promotions (external https://beta-promo.coral.co.uk/en/promo/offers)
        EXPECTED: * Voucher Code opens Voucher page (https://beta-sports.coral.co.uk/voucher-code)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Free Bets opens Free Bets page
        EXPECTED: * Odds Boost opens Odds Boost page
        EXPECTED: * Sports Promotions opens Promotions page
        EXPECTED: * Gaming Promotions opens Gaming promotions (external https://promo.ladbrokes.com/en/promo/offers)
        """
        pass

    def test_006_ladbrokes_go_back_and_open_my_account_menu_clicktap_on_sports_free_bets_item(self):
        """
        DESCRIPTION: **Ladbrokes**
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Sports Free Bets' item
        EXPECTED: 'Sports Free Bets' opens Free Bets page
        """
        pass

    def test_007_ladbrokes_go_back_and_open_my_account_menu_clicktap_on_odds_boosts_item(self):
        """
        DESCRIPTION: **Ladbrokes**
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Odds Boosts' item
        EXPECTED: 'Odds Boosts' opens Odds Boosts page
        """
        pass

    def test_008_ladbrokes_go_back_and_open_my_account_menu_clicktap_on_my_bets_item(self):
        """
        DESCRIPTION: **Ladbrokes**
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'My Bets' item
        EXPECTED: 'My Bets' opens My Bets page
        """
        pass

    def test_009__go_back_and_open_my_account_menu_clicktap_on_history_item(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click/Tap on 'History' item
        EXPECTED: 'History' Overlay/pop-up is opened with the following items:
        EXPECTED: **Coral**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Betting History
        EXPECTED: * Transaction History
        EXPECTED: * Payment History
        EXPECTED: ![](index.php?/attachments/get/115421428)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Betting History
        EXPECTED: * Payment History
        EXPECTED: * Transactions History
        EXPECTED: ![](index.php?/attachments/get/115421452)
        """
        pass

    def test_010_verify_every_item_menu_navigation_by_clickingtapping_on_it(self):
        """
        DESCRIPTION: Verify every item menu navigation by clicking/tapping on it
        EXPECTED: * Betting History opens Settled Bets page/tab
        EXPECTED: * Transaction History opens Gaming history ( e.g. https://beta-sports.coral.co.uk/en/mobileportal/transactions)
        EXPECTED: * Payment History opens Payment history page ( e.g. https://cashier.coral.co.uk/home/txnSearchPageMerchant.action?sessionKey=198d8026e07f487fb348c516cc3d355a&LANG_ID=en&parent=https://beta-sports.coral.co.uk/)
        """
        pass

    def test_011__go_back_and_open_my_account_menu_clicktap_on_messages_item(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Messages' item
        EXPECTED: 'Messages' overlay/pop-up is opened with rich inbox messages available or 'You have no messages!' in case messages are not available
        """
        pass

    def test_012__go_back_and_open_my_account_menu_clicktap_on_connectthe_grid_item(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Connect'/'The Grid' item
        EXPECTED: 'Connect' Overlay/pop-up is opened with the following items:
        EXPECTED: **Coral**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Shop Exclusive Promos
        EXPECTED: * Shop Bet Tracker
        EXPECTED: * Football Bet Filter
        EXPECTED: * Shop Locator
        EXPECTED: ![](index.php?/attachments/get/115421482)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * The Grid Home
        EXPECTED: * Join Grid
        EXPECTED: * My Payout Settings
        EXPECTED: * Shop Locator
        EXPECTED: ![](index.php?/attachments/get/115421484)
        """
        pass

    def test_013_verify_every_item_menu_navigation_by_clickingtapping_on_it(self):
        """
        DESCRIPTION: Verify every item menu navigation by clicking/tapping on it
        EXPECTED: **Coral**
        EXPECTED: * Shop Exclusive Promos opens Promotions page > Shop Exclusive tab
        EXPECTED: * Shop Bet Tracker opens Shop Bet Tracker page
        EXPECTED: * Football Bet Filter opens Football Bet Filter page
        EXPECTED: * Shop Locator opens Shop Locator page with map opened
        EXPECTED: **Ladbrokes**
        EXPECTED: * The Grid Home opens external link (e.g. https://thegrid.ladbrokes.com/en)
        EXPECTED: * Join Grid opens Generate Grid card page (e.g. https://sports.ladbrokes.com/en/mobileportal/virtualcard)
        EXPECTED: * My Payout Settings opens the Payout settings page (e.g. http://sports.ladbrokes.com/en/mobileportal/payoutsettings)
        EXPECTED: * Shop Locator opens Shop Locator page with map opened
        """
        pass

    def test_014__go_back_and_open_my_account_menu_click_on_settings_item(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click on 'Settings' item
        EXPECTED: 'Settings'Overlay/pop-up is opened with the following items:
        EXPECTED: **Coral**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * My Account Details
        EXPECTED: * Change Password
        EXPECTED: * Marketing Preferences
        EXPECTED: * Betting Setting
        EXPECTED: ![](index.php?/attachments/get/115421553)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * My Account Details
        EXPECTED: * Change Password
        EXPECTED: * Communication Preferences
        EXPECTED: * Betting Setting
        EXPECTED: ![](index.php?/attachments/get/115421556)
        """
        pass

    def test_015_verify_every_item_menu_navigation_by_clickingtapping_on_it(self):
        """
        DESCRIPTION: Verify every item menu navigation by clicking/tapping on it
        EXPECTED: * My Account Details opens My account details overlay/pop-up
        EXPECTED: * Change Password opens Change Password overlay/pop-up
        EXPECTED: * Marketing/Communication Preferences opens  Communication Preferences
        EXPECTED: * Betting Setting opens Preferences Page
        """
        pass

    def test_016__go_back_and_open_my_account_menu_clicktap_on_gambling_controls(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Gambling controls'
        EXPECTED: 'Gambling Controls' Overlay/Pop-up is opened
        EXPECTED: ![](index.php?/attachments/get/115421561)
        EXPECTED: ![](index.php?/attachments/get/115421562)
        """
        pass

    def test_017__go_back_and_open_my_account_menu_clicktap_on_help__contact(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Help & Contact'
        EXPECTED: 'Help & Contact' Overlay/Pop-up is opened
        EXPECTED: ![](index.php?/attachments/get/115421563)
        EXPECTED: ![](index.php?/attachments/get/115421564)
        """
        pass

    def test_018__go_back_and_open_my_account_menu_clicktap_on_log_out(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Log Out'
        EXPECTED: User is logged out
        """
        pass

    def test_019__go_back_and_open_my_account_menu_clicktap_on_deposit_button(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Deposit' button
        EXPECTED: 'Deposit' button opens deposit Overlay/pop-up
        """
        pass
