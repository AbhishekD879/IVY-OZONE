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
class Test_C2988052_Verify_redirection_to_from_Deposit_page_on_Account_One_portal(Common):
    """
    TR_ID: C2988052
    NAME: Verify redirection to/from 'Deposit' page on 'Account One' portal
    DESCRIPTION: This test case verifies redirection from 'Roxanne' app to 'Deposit' page on IMS 'Account One' portal via 'Deposit' menu items/links across an app
    PRECONDITIONS: 1. In CMS > System Configuration > Structure: 'Account One' section with 'Field Name' = 'deposit' & 'Field Value' = [account one url e.g. http://accountone-test.ladbrokes.com/deposit] is available
    PRECONDITIONS: 2. Roxanne app is loaded
    PRECONDITIONS: 3. User with 0 balance & no credit cards added is logged into an app
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link & creds to Ladbrokes IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: - Account One redirection urls:
    PRECONDITIONS: * TST2: http://accountone-test.ladbrokes.com/deposit?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * STG: https://accountone-stg.ladbrokes.com/deposit?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * PROD: http://accountone.ladbrokes.com/deposit?clientType=sportsbook&back_url=[url to an app]
    """
    keep_browser_open = True

    def test_001_tap_on_deposit_link_on_quick_deposit_pop_up(self):
        """
        DESCRIPTION: Tap on 'Deposit' link on 'Quick Deposit' pop up
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Deposit' page
        EXPECTED: **Desktop**
        EXPECTED: 'Account One' portal > 'Deposit' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_002_mobiletablettap_on_close_icon_in_the_right_upper_corner_of_deposit_page_on_account_one_portaldesktopclose_the_deposit_account_one_portal_pop_up(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'Deposit' page (on 'Account One' portal)
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Close the 'Deposit' ('Account One' portal) pop up
        EXPECTED: - User is redirected back to an app
        EXPECTED: - The app is refreshed > splash screen is displayed
        EXPECTED: - User is landed on the page from which he was redirected
        EXPECTED: - Balance is not changed
        EXPECTED: **Desktop:**
        EXPECTED: Pop up is closed & app is NOT refreshed, when closing by 'X' outside icon
        """
        pass

    def test_003_mobiletablettap_on_right_menu__deposit_button(self):
        """
        DESCRIPTION: **Mobile&Tablet**
        DESCRIPTION: Tap on 'Right Menu' > 'Deposit' button
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Deposit' page
        EXPECTED: **Desktop**
        EXPECTED: 'Account One' portal > 'Deposit' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_004_tap_on_close_icon_in_the_right_upper_corner_of_deposit_page_on_account_one_portal(self):
        """
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'Deposit' page (on 'Account One' portal)
        EXPECTED: - User is redirected back to an app
        EXPECTED: - The app is refreshed > splash screen is displayed
        EXPECTED: - User is landed on the page from which he was redirected
        EXPECTED: - Balance is not changed
        """
        pass

    def test_005_mobiletablettap_on_the_right_menu__banking__deposit_menu_itemdesktopclick_on_my_account__banking__deposit_menu_item(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on the 'Right Menu' > 'Banking' > 'Deposit' menu item
        DESCRIPTION: **Desktop**
        DESCRIPTION: Click on 'My Account' > 'Banking' > 'Deposit' menu item
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Deposit' page
        EXPECTED: **Desktop**
        EXPECTED: 'Account One' portal > 'Deposit' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_006_mobiletablettap_on_close_icon_in_the_right_upper_corner_of_deposit_page_on_account_one_portaldesktopclose_the_deposit_account_one_portal_pop_up(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'Deposit' page (on 'Account One' portal)
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Close the 'Deposit' ('Account One' portal) pop up
        EXPECTED: - User is redirected back to an app
        EXPECTED: - The app is refreshed > splash screen is displayed
        EXPECTED: - User is landed on the page from which he was redirected
        EXPECTED: - Balance is not changed
        EXPECTED: **Desktop:**
        EXPECTED: Pop up is closed & app is NOT refreshed, when closing by 'X' outside icon
        """
        pass

    def test_007_desktoptap_on_quick_deposit_menu(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Tap on 'Quick Deposit' menu
        EXPECTED: 'Account One' portal > 'Deposit' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_008_close_the_deposit_account_one_portal_pop_up(self):
        """
        DESCRIPTION: Close the 'Deposit' ('Account One' portal) pop up
        EXPECTED: - User is redirected back to an app
        EXPECTED: - The app is refreshed > splash screen is displayed
        EXPECTED: - User is landed on the page from which he was redirected
        EXPECTED: - Balance is not changed
        EXPECTED: **Desktop:**
        EXPECTED: Pop up is closed & app is NOT refreshed, when closing by 'X' outside icon
        """
        pass

    def test_009_mobiletablet__go_to_any_sports_page__add_selections_to_the_betslip__open_betslip_tap_account_balance_area_in_the_betslip_header__deposit_button(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: - Go to any <Sports> page
        DESCRIPTION: - Add selections to the Betslip
        DESCRIPTION: - Open Betslip
        DESCRIPTION: > Tap 'Account Balance' area in the Betslip header > Deposit button
        EXPECTED: User is redirected to 'Account One' portal > 'Deposit' page
        """
        pass

    def test_010_tap_on_close_icon_in_the_right_upper_corner_of_deposit_page_on_account_one_portal(self):
        """
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'Deposit' page (on 'Account One' portal)
        EXPECTED: - User is redirected back to an app
        EXPECTED: - The app is refreshed > splash screen is displayed
        EXPECTED: - User is landed on the page from which he was redirected
        EXPECTED: - Balance is not changed
        """
        pass
