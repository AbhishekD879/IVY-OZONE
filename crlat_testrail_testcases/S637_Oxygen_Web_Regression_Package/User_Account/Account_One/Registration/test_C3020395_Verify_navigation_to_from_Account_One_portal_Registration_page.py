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
class Test_C3020395_Verify_navigation_to_from_Account_One_portal_Registration_page(Common):
    """
    TR_ID: C3020395
    NAME: Verify navigation to/from 'Account One' portal 'Registration' page
    DESCRIPTION: This test case verifies redirection from 'Roxanne' app to 'Registration' page on IMS 'Account One' portal via 'Join now' button
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
        DESCRIPTION: For **Ladbrokes (Mobile and Desktop)**:
        DESCRIPTION: Click on 'Register' button
        EXPECTED: User is redirected to 'Account One' portal >'Registraion' page
        """
        pass

    def test_002_populate_some_fields(self):
        """
        DESCRIPTION: Populate some fields
        EXPECTED: Fields are successfully populated
        """
        pass

    def test_003_clicks_on_the_x_during_the_registration_process_or_save__continue_later(self):
        """
        DESCRIPTION: Clicks on the 'X' during the registration process OR 'Save & Continue Later'
        EXPECTED: * User is navigated back to an app
        EXPECTED: * User is logged out
        """
        pass
