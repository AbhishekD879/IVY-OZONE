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
class Test_C8141144_Verify_navigation_to_from_Account_one_portal_via_Deposit_button(Common):
    """
    TR_ID: C8141144
    NAME: Verify navigation to/from 'Account' one portal via 'Deposit' button
    DESCRIPTION: This test case verifies navigation to/from 'Account One' portal via 'Deposit' button on 'Right' menu, when no credit cards are added to a user account.
    DESCRIPTION: AUTOTEST: C15785355
    PRECONDITIONS: 1. In CMS > System Configuration > Structure: 'ExternalUrls' section with 'Field Name' = 'deposit' & 'Field Value' = [account one url e.g. http://accountone-test.ladbrokes.com/deposit] is available
    PRECONDITIONS: 2. Roxanne app is loaded
    PRECONDITIONS: 3. User is logged into an app
    PRECONDITIONS: 4. User doesn't have credit cards added to his account
    PRECONDITIONS: **Quick deposit is only for mobile**
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - If user has credit card already added, quick deposit window will be used instead of redirection to Account One (when using green button 'Deposit')
    PRECONDITIONS: - Test Accounts for Payment methods: https://confluence.egalacoral.com/display/SPI/Test+Accounts+for+Payments+Functionality+Testing
    PRECONDITIONS: - Link & creds to Ladbrokes IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: Account One redirection URLs:
    PRECONDITIONS: TST2: http://accountone-test.ladbrokes.com/deposit?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: STG: https://accountone-stg.ladbrokes.com/deposit?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: PROD: http://accountone.ladbrokes.com/deposit?clientType=sportsbook&back_url=[url to an app]
    """
    keep_browser_open = True

    def test_001_tap_right_menu__verify_deposit_button(self):
        """
        DESCRIPTION: Tap 'Right Menu' > Verify 'Deposit' button
        EXPECTED: * Right menu is opened
        EXPECTED: * 'Deposit' button is present in the top part of the page
        """
        pass

    def test_002_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: User is redirected to 'Account One' portal > 'Deposit' page
        """
        pass

    def test_003_tap_on_close_icon_in_the_right_upper_corner_of_deposit_page_on_account_one_portal(self):
        """
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'Deposit' page (on 'Account One' portal)
        EXPECTED: User is navigated back to an app to the page he came from
        """
        pass
