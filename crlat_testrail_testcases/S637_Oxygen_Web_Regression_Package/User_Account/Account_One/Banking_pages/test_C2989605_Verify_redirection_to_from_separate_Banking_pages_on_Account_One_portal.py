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
class Test_C2989605_Verify_redirection_to_from_separate_Banking_pages_on_Account_One_portal(Common):
    """
    TR_ID: C2989605
    NAME: Verify redirection to/from separate 'Banking' pages on 'Account One' portal
    DESCRIPTION: This test case verifies redirection from 'Roxanne' app to 'Banking' pages on IMS 'Account One' portal via 'Transfer', 'Withdraw', 'Banking History', 'Deposit Limits', View Balances' links in the app
    DESCRIPTION: AUTOTEST
    DESCRIPTION: Mobile [C16396580]
    DESCRIPTION: Desktop [C16396579]
    PRECONDITIONS: 1. In CMS > System Configuration > Structure: 'ExternalUrls' section with 'Field Name' = the name of one of Banking links (e.g.'Transfer', 'Withdraw', 'Banking History', 'Deposit Limits', View Balances')  & 'Field Value' = [account one url e.g., http://accountone-test.ladbrokes.com/deposit] is available
    PRECONDITIONS: 2. Roxanne app is loaded
    PRECONDITIONS: 3. User is logged in
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link & creds to Ladbrokes IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: * Account One redirection urls:
    PRECONDITIONS: * TST2: http://accountone-test.ladbrokes.com/one of Banking links (e.g. 'Transfer', 'Withdraw', 'Banking History', 'Deposit Limits', View Balances')?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * STG: https://accountone-stg.ladbrokes.com/one of Banking links (e.g. 'Transfer', 'Withdraw', 'Banking History', 'Deposit Limits', View Balances')?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * PROD: http://accountone.ladbrokes.com/one of Banking links (e.g. 'Transfer', 'Withdraw', 'Banking History', 'Deposit Limits', View Balances')?clientType=sportsbook&back_url=[url to an app]
    """
    keep_browser_open = True

    def test_001_mobiletablettap_on_the_right_menu__transfer_menu_itemdesktopclick_on_my_account__transfer_menu_item(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on the 'Right Menu' > **'Transfer'** menu item
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Click on 'My Account' > 'Transfer' menu item
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Transfer' page
        EXPECTED: **Desktop:**
        EXPECTED: 'Account One' portal > 'Transfer' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_002_mobiletablettap_on_close_icon_in_the_right_upper_corner_of_transfer_page_on_account_one_portaldesktopclose_the_transfer_account_one_portal_pop_up(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'Transfer' page (on 'Account One' portal)
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Close the 'Transfer' ('Account One' portal) pop up
        EXPECTED: * User is redirected back to the app
        EXPECTED: * User is landed on the page he came from
        EXPECTED: * Balance is not changed
        """
        pass

    def test_003_mobiletablettap_on_the_right_menu__withdraw_menu_itemdesktopclick_on_my_account__withdraw_menu_item(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on the 'Right Menu' > **'Withdraw'** menu item
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Click on 'My Account' > 'Withdraw' menu item
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Withdraw' page
        EXPECTED: **Desktop:**
        EXPECTED: 'Account One' portal > 'Withdraw' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_004_mobiletablettap_on_close_icon_in_the_right_upper_corner_of_withdraw_page_on_account_one_portaldesktopclose_the_withdraw_account_one_portal_pop_up(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'Withdraw' page (on 'Account One' portal)
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Close the 'Withdraw' ('Account One' portal) pop up
        EXPECTED: * User is redirected back to the app
        EXPECTED: * User is landed on the page he came from
        EXPECTED: * Balance is not changed
        """
        pass

    def test_005_mobiletablettap_on_the_right_menu__banking_history_menu_itemdesktopclick_on_my_account__banking_history_menu_item(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on the 'Right Menu' > **'Banking History'** menu item
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Click on 'My Account' > 'Banking History' menu item
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Banking History' page
        EXPECTED: **Desktop:**
        EXPECTED: 'Account One' portal > 'Banking History' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_006_mobiletablettap_on_close_icon_in_the_right_upper_corner_of_banking_history_page_on_account_one_portaldesktopclose_the_banking_history_account_one_portal_pop_up(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'Banking History' page (on 'Account One' portal)
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Close the 'Banking History' ('Account One' portal) pop up
        EXPECTED: * User is redirected back to the app
        EXPECTED: * User is landed on the page he came from
        EXPECTED: * Balance is not changed
        """
        pass

    def test_007_mobiletablettap_on_the_right_menu__view_balance_menu_itemdesktopclick_on_my_account__view_balance_menu_item(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on the 'Right Menu' > **'View Balance'** menu item
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Click on 'My Account' > 'View Balance' menu item
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'View Balance' page
        EXPECTED: **Desktop:**
        EXPECTED: 'Account One' portal > 'View Balance' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_008_mobiletablettap_on_close_icon_in_the_right_upper_corner_of_view_balance_page_on_account_one_portaldesktopclose_the_view_balance_account_one_portal_pop_up(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'View Balance' page (on 'Account One' portal)
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Close the 'View Balance' ('Account One' portal) pop up
        EXPECTED: * User is redirected back to the app
        EXPECTED: * User is landed on the page he came from
        EXPECTED: * Balance is not changed
        """
        pass
