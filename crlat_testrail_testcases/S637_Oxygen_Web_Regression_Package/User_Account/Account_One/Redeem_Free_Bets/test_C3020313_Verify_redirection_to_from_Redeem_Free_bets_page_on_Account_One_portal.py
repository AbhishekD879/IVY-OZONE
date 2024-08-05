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
class Test_C3020313_Verify_redirection_to_from_Redeem_Free_bets_page_on_Account_One_portal(Common):
    """
    TR_ID: C3020313
    NAME: Verify redirection to/from 'Redeem Free bets' page on 'Account One' portal
    DESCRIPTION: This test case verifies redirection from 'Roxanne' app to 'Free bets' page on IMS 'Account One' portal via 'Free bets' menu on 'MyAccount' page
    DESCRIPTION: AUTOTEST:
    DESCRIPTION: Mobile [C22671833]
    DESCRIPTION: Desktop [C22671835]
    PRECONDITIONS: 1. In CMS > System Configuration > Structure: 'Account One' section with 'Field Name' = 'freebets' & 'Field Value' = [account one url e.g. https://accountone.ladbrokes.com/free-bets] is available
    PRECONDITIONS: 2. Roxanne app is loaded
    PRECONDITIONS: 3. User is logged into an app
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link & creds to Ladbrokes IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: - Account One redirection urls:
    PRECONDITIONS: * TST2: http://accountone-test.ladbrokes.com/free-bets?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * STG: https://accountone-stg.ladbrokes.com/free-bets?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * PROD: http://accountone.ladbrokes.com/free-bets?clientType=sportsbook&back_url=[url to an app]
    """
    keep_browser_open = True

    def test_001_mobiletablettap_on_the_right_menu__redeem_free_bets_menu_itemdesktopclick_on_my_account__redeem_free_bets_menu_item(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on the 'Right Menu' > 'Redeem Free Bets' menu item
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Click on 'My Account' > 'Redeem Free Bets' menu item
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Free Bets' page
        EXPECTED: **Desktop:**
        EXPECTED: 'Account One' portal > ''Redeem Free Bets' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_002_tap_close_button_x(self):
        """
        DESCRIPTION: Tap 'Close' button (X)
        EXPECTED: * User is navigated back to the same page of an app from where he was redirected
        EXPECTED: * User is logged in
        """
        pass
