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
class Test_C62764786_Verify_navigation_between_Non_CSP_and_CSP_modules(Common):
    """
    TR_ID: C62764786
    NAME: Verify navigation between Non CSP and CSP modules
    DESCRIPTION: This test case verifies navigation between CSP and Non CSP modules
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> surface bet
    PRECONDITIONS: 2)Create a some Segmented and universal surface bets
    PRECONDITIONS: 3)Should enabled  some Non CSP modules
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_precondition(self):
        """
        DESCRIPTION: Navigate to module from precondition
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_surface_bet_link(self):
        """
        DESCRIPTION: Click on surface bet link.
        EXPECTED: User should be able to view existing surface bets should be displayed.
        """
        pass

    def test_004_verify_non_csp_in_cms__exinplay(self):
        """
        DESCRIPTION: Verify Non CSP in CMS ( ex:Inplay)
        EXPECTED: Non CSP modules should be enabled in CMS
        """
        pass

    def test_005_launch_the_oxygen_application_verify_non_csp_and_csp_modules(self):
        """
        DESCRIPTION: Launch the Oxygen application ,Verify Non CSP and CSP modules
        EXPECTED: Non CSP modules should be shown in universal view
        """
        pass

    def test_006_verify_navigation_between_csp_and_non_csp_modules(self):
        """
        DESCRIPTION: Verify Navigation between CSP and Non CSP modules
        EXPECTED: Navigation should be smooth
        """
        pass
