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
class Test_C3020393_Verify_successful_registration_through_Account_One_portal(Common):
    """
    TR_ID: C3020393
    NAME: Verify successful registration through 'Account One' portal
    DESCRIPTION: This test case verifies successful user registration
    PRECONDITIONS: 1. In CMS > System Configuration > Structure: 'Account One' section with 'Field Name' = 'signup' & 'Field Value' = [account one url e.g. http://accountone-test.ladbrokes.com/register] is available
    PRECONDITIONS: 2. Roxanne app is loaded
    PRECONDITIONS: 3. User is logged out
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link & creds to Ladbrokes IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: - Account One redirection urls:
    PRECONDITIONS: * TST2: http://accountone-test.ladbrokes.com/register?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * STG: https://accountone-stg.ladbrokes.com/register?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * PROD: http://accountone.ladbrokes.com/register?clientType=sportsbook&back_url=[url to an app]
    """
    keep_browser_open = True

    def test_001_mobiletap_loginjoin_button__join_us_here_buttondesktopclick_join_now_buttonfor_ladbrokes_mobile_and_desktopclick_on_register_button(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Tap 'Login/Join' button > 'Join us here' button
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Click 'Join now' button
        DESCRIPTION: **For Ladbrokes (Mobile and Desktop)**:
        DESCRIPTION: Click on 'Register' button
        EXPECTED: Account One Registration page is displayed
        """
        pass

    def test_002_complete_the_3_step_registration_processand_tap_the_button_open_account(self):
        """
        DESCRIPTION: Complete the 3 step registration process
        DESCRIPTION: and tap the button 'Open account'
        EXPECTED: 'Save my preferences' page is opened
        """
        pass

    def test_003_fill_the_contact_preference_page__tap_save_my_preferences(self):
        """
        DESCRIPTION: Fill the 'Contact Preference Page' > tap 'Save my preferences'
        EXPECTED: **Mobile:**
        EXPECTED: Account One Deposit page is displayed
        EXPECTED: **Desktop:**
        EXPECTED: * User is navigated back to an app
        EXPECTED: * User is logged in with registered credentials
        """
        pass

    def test_004_close_account_one_deposit_page(self):
        """
        DESCRIPTION: Close 'Account One Deposit' page
        EXPECTED: * User is navigated back to an app
        EXPECTED: * User is logged in with registered credentials
        """
        pass
