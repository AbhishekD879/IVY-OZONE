import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C87324_Verify_windowgcData_data_layer_object(Common):
    """
    TR_ID: C87324
    NAME: Verify 'window.gcData' data layer object
    DESCRIPTION: This test case verifies 'window.gcData' data layer object
    DESCRIPTION: JIRA TICKETS:
    DESCRIPTION: BMA-15239 Update Data Layer
    PRECONDITIONS: 1. Clear browser cookies
    PRECONDITIONS: 2. Load Oxygen application and go to Console
    PRECONDITIONS: 3. In Console window type 'window.gcData' and press Enter button
    PRECONDITIONS: 4. Expand 'Object'
    PRECONDITIONS: For detection **region** value use http://www.nationsonline.org/oneworld/country_code_list.htm link where you can find Alpha-2 country code (e.g. UK, GI).
    PRECONDITIONS: Note, **profileID** = 'advertiser' attribute returns the same value for all users - 'default9c' on prod env, 'default5c' on tst2 env (see in IMS).
    PRECONDITIONS: Also, **loginID** = 'sessionToken' attribute in IMS or response ID 31002 in Network -> WS; **customerID** = 'playerCode' attribute in IMS or response ID 31002 in Network -> WS.
    """
    keep_browser_open = True

    def test_001_verify_new_data_object_for_logged_out_users_who_have_not_registered_before(self):
        """
        DESCRIPTION: Verify new data object for logged out users who have **NOT** registered before
        EXPECTED: The datalayer values are set as follows:
        EXPECTED: **brand:** 'Coral'
        EXPECTED: **convertibleUser:** 'True'
        EXPECTED: **currency:** 'GBR'
        EXPECTED: **customerID:** 'null'
        EXPECTED: **email:** 'null'
        EXPECTED: **firstName:** 'null'
        EXPECTED: **lastName:** 'null'
        EXPECTED: **loggedIn:** 'false'
        EXPECTED: **postCode:** 'null'
        EXPECTED: **loginID:** 'null'
        EXPECTED: **profileID:** 'null'
        EXPECTED: **region:** 'null'
        EXPECTED: **signUpDeliveryPlatform:** 'HTML5' (for all desktop, tablet and mobile users) and 'Wrapper' (for all Wrapped App users)
        EXPECTED: **userInterface:** 'HTML5' (for all desktop, tablet and mobile users) and 'Wrapped App' (for all Wrapped App users)
        EXPECTED: **userInterfaceName:** 'Oxygen' (for all users)
        EXPECTED: **userType:** 'Visitor'
        EXPECTED: **username:** 'null'
        EXPECTED: **vipLevel:** 'null'
        """
        pass

    def test_002_verify_new_data_object_for_logged_out_users_who_have_registered_before(self):
        """
        DESCRIPTION: Verify new data object for logged out users who have registered before
        EXPECTED: The datalayer values are set as follows:
        EXPECTED: **brand:** 'Coral'
        EXPECTED: **convertibleUser:** 'False'
        EXPECTED: **currency:** 'GBR'/'EUR'/'USD'/etc.
        EXPECTED: **customerID:** 'null'
        EXPECTED: **email:** 'null'
        EXPECTED: **firstName:** 'null'
        EXPECTED: **lastName:** 'null'
        EXPECTED: **loggedIn:** 'false'
        EXPECTED: **postCode:** 'null'
        EXPECTED: **loginID:** 'null'
        EXPECTED: **profileID:** 'null'
        EXPECTED: **region:** 'null'
        EXPECTED: **signUpDeliveryPlatform:** 'HTML5' (for all desktop, tablet and mobile users) and 'Wrapper' (for all Wrapped App users)
        EXPECTED: **userInterface:** 'HTML5' (for all desktop, tablet and mobile users) and 'Wrapped App' (for all Wrapped App users)
        EXPECTED: **userInterfaceName:** 'Oxygen' (for all users)
        EXPECTED: **userType:** 'Browsing Customer'
        EXPECTED: **username:** 'null'
        EXPECTED: **vipLevel:** 'null'
        """
        pass

    def test_003_verify_new_data_object_for_logged_in_users(self):
        """
        DESCRIPTION: Verify new data object for logged in users
        EXPECTED: The datalayer values are set as follows:
        EXPECTED: **brand:** 'Coral'
        EXPECTED: **convertibleUser:** 'False'
        EXPECTED: **currency:** 'GBR'/'EUR'/'USD'/etc.
        EXPECTED: **customerID:** '#####' (this is User.playerCode in IMS)
        EXPECTED: **email:** ' ' (users email address from IMS)
        EXPECTED: **firstName:** ' ' (users first name from IMS)
        EXPECTED: **lastName:** ' ' (users last name from IMS)
        EXPECTED: **loggedIn:** 'true'
        EXPECTED: **postCode:** ' ' ( users post code from IMS)
        EXPECTED: **loginID:** '##### ' (this is User.sessionToken in IMS)
        EXPECTED: **profileID:** '#####' (this value is the profile ID from IMS)
        EXPECTED: **region:** 'country code' (e.g. UK, GI)
        EXPECTED: **signUpDeliveryPlatform:** 'HTML5' (for all desktop, tablet and mobile users) and 'Wrapper' (for all Wrapped App users)
        EXPECTED: **userInterface:** 'HTML5' (for all desktop, tablet and mobile users) and 'Wrapped App' (for all Wrapped App users)
        EXPECTED: **userInterfaceName:** 'Oxygen' (for all users)
        EXPECTED: **userType:** 'Logged In Customer'
        EXPECTED: **username:** (users username from IMS)
        EXPECTED: **vipLevel:** 'e.g. 11, 12,13'
        """
        pass

    def test_004_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Page is refreshed
        EXPECTED: User is still Logged In
        """
        pass

    def test_005_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step 3
        EXPECTED: 
        """
        pass
