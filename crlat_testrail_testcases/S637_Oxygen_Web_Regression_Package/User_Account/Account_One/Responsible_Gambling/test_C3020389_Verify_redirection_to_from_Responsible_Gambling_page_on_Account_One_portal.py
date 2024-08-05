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
class Test_C3020389_Verify_redirection_to_from_Responsible_Gambling_page_on_Account_One_portal(Common):
    """
    TR_ID: C3020389
    NAME: Verify redirection to/from 'Responsible Gambling' page on 'Account One' portal
    DESCRIPTION: This test case verifies redirection from 'Roxanne' app to 'Responsible Gambling' page on IMS 'Account One' portal and back to an app
    DESCRIPTION: AUTO TEST MOBILE: [C30987272]
    DESCRIPTION: DESKTOP: [C31220749]
    PRECONDITIONS: 1. In CMS > System Configuration > Structure: 'Account One' section with 'Field Name' = 'responsible-gambling' & 'Field Value' = [account one url e.g. http://accountone-test.ladbrokes.com/responsible-gambling] is available
    PRECONDITIONS: 2. Roxanne app is loaded
    PRECONDITIONS: 3. User is logged in
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link & creds to Ladbrokes IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: - Account One redirection urls:
    PRECONDITIONS: * TST2: http://accountone-test.ladbrokes.com/responsible-gambling?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * STG: https://accountone-stg.ladbrokes.com/responsible-gambling?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * PROD: http://accountone.ladbrokes.com/responsible-gambling?clientType=sportsbook&back_url=[url to an app]
    """
    keep_browser_open = True

    def test_001_mobiletablettap_on_right_menu__responsible_gambling_menu_itemdesktopclick_on_my_account__responsible_gambling_menu_item(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on 'Right Menu' > 'Responsible Gambling' menu item
        DESCRIPTION: **Desktop**
        DESCRIPTION: Click on 'My Account' > 'Responsible Gambling' menu item
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Responsible Gambling' page
        EXPECTED: **Desktop**
        EXPECTED: 'Account One' portal > 'Responsible Gambling' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_002_mobiletablettap_on_close_icon_in_the_right_upper_corner_of_responsible_gambling_page_on_account_one_portaldesktopclose_the_deposit_account_one_portal_pop_up(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'Responsible Gambling' page (on 'Account One' portal)
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Close the 'Deposit' ('Account One' portal) pop up
        EXPECTED: - User is redirected back to an app
        EXPECTED: - The app is refreshed > splash screen is displayed
        EXPECTED: - User is landed on the page from which he was redirected
        EXPECTED: - User remains logged in
        """
        pass

    def test_003_mobiletablettap_on_right_menu__banking__deposit_limit_menu_itemdesktopclick_on_my_account__deposit_limit_menu_item(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on 'Right Menu' > 'Banking' > 'Deposit Limit' menu item
        DESCRIPTION: **Desktop**
        DESCRIPTION: Click on 'My Account' > 'Deposit Limit' menu item
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Responsible Gambling' page
        EXPECTED: **Desktop**
        EXPECTED: 'Account One' portal > 'Responsible Gambling' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_004_mobiletablettap_on_close_icon_in_the_right_upper_corner_of_responsible_gambling_page_on_account_one_portaldesktopclose_the_deposit_account_one_portal_pop_up(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'Responsible Gambling' page (on 'Account One' portal)
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Close the 'Deposit' ('Account One' portal) pop up
        EXPECTED: - User is redirected back to an app
        EXPECTED: - The app is refreshed > splash screen is displayed
        EXPECTED: - User is landed on the page from which he was redirected
        EXPECTED: - User remains logged in
        """
        pass

    def test_005_mobiletablet__add_a_selection_to_quick_bet__enter_amount_that_exceeds_users_balance__open_quick_deposit__tap_on_set_my_deposit_limits_link_within_quick_deposit(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: - Add a selection to 'Quick Bet'
        DESCRIPTION: - Enter amount that exceeds user's balance
        DESCRIPTION: - Open 'Quick Deposit'
        DESCRIPTION: - Tap on 'Set my deposit limits' link within 'Quick Deposit'
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Responsible Gambling' page
        EXPECTED: **Desktop**
        EXPECTED: 'Account One' portal > 'Responsible Gambling' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_006_tap_on_close_icon_in_the_right_upper_corner_of_responsible_gambling_page_on_account_one_portal(self):
        """
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'Responsible Gambling' page (on 'Account One' portal)
        EXPECTED: - User is redirected back to an app
        EXPECTED: - The app is refreshed > splash screen is displayed
        EXPECTED: - User is landed on the page from which he was redirected
        EXPECTED: - User remains logged in
        """
        pass

    def test_007___add_selections_to_the_betslip__open_betslip__enter_amount_that_exceeds_users_balance__open_quick_deposit__tap_on_set_my_deposit_limits_link_within_quick_deposit(self):
        """
        DESCRIPTION: - Add selection(s) to the Betslip
        DESCRIPTION: - Open 'Betslip'
        DESCRIPTION: - Enter amount that exceeds user's balance
        DESCRIPTION: - Open 'Quick Deposit'
        DESCRIPTION: - Tap on 'Set my deposit limits' link within 'Quick Deposit'
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Responsible Gambling' page
        EXPECTED: **Desktop**
        EXPECTED: 'Account One' portal > 'Responsible Gambling' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_008_mobiletablettap_on_close_icon_in_the_right_upper_corner_of_responsible_gambling_page_on_account_one_portaldesktopclose_the_deposit_account_one_portal_pop_up(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'Responsible Gambling' page (on 'Account One' portal)
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Close the 'Deposit' ('Account One' portal) pop up
        EXPECTED: - User is redirected back to an app
        EXPECTED: - The app is refreshed > splash screen is displayed
        EXPECTED: - User is landed on the page from which he was redirected
        EXPECTED: - User remains logged in
        """
        pass
