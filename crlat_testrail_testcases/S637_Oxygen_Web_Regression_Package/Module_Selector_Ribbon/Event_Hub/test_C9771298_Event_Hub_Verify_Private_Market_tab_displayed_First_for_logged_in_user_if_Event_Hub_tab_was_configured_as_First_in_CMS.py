import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9771298_Event_Hub_Verify_Private_Market_tab_displayed_First_for_logged_in_user_if_Event_Hub_tab_was_configured_as_First_in_CMS(Common):
    """
    TR_ID: C9771298
    NAME: Event Hub: Verify Private Market tab displayed First for logged in user if Event Hub tab was configured as First in CMS
    DESCRIPTION: This test case verifies that Private Market tab is displayed First for logged in user if Event Hub tab was configured as First in CMS
    PRECONDITIONS: 1. Event Hub is created on CMS > Sport Pages > Event Hub
    PRECONDITIONS: 2. Module ribbon tab is configured and has Event Hub mapped. THis Module ribbon tab is configured ti be displayed First on FE.
    PRECONDITIONS: 3. User with Private Markets configured exists. (https://confluence.egalacoral.com/display/SPI/How+to+Setup+and+Use+Private+Markets)
    """
    keep_browser_open = True

    def test_001_load_app_as_logged_out_user_navigate_to_homepage_and_verify_module_ribbon_tab_from_preconditions(self):
        """
        DESCRIPTION: Load app as logged out user, navigate to Homepage and Verify Module ribbon tab from preconditions
        EXPECTED: Event Hub Module ribbon tab is displayed first in ribbon.
        EXPECTED: User lands on this tab when he loads app.
        """
        pass

    def test_002_login_as_user_from_preconditions(self):
        """
        DESCRIPTION: Login as user from preconditions
        EXPECTED: * User logged in
        EXPECTED: * Your Enhanced Markets tab appears in ribbon before Event Hub tab.
        EXPECTED: * User remains on Event Hub tab
        """
        pass

    def test_003_navigate_somewhere_else_in_the_app_and_back_to_homepage(self):
        """
        DESCRIPTION: Navigate somewhere else in the app and back to Homepage
        EXPECTED: * User lands on Your Enhanced Markets tab.
        """
        pass
