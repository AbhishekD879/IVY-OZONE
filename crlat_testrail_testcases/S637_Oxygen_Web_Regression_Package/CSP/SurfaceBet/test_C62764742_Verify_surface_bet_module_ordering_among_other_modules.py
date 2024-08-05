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
class Test_C62764742_Verify_surface_bet_module_ordering_among_other_modules(Common):
    """
    TR_ID: C62764742
    NAME: Verify surface bet module ordering among other modules
    DESCRIPTION: Test case verifies possibility to order surface bet module among other modules
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: CMS configuration&gt;
    PRECONDITIONS: CMS &gt; sports pages &gt;home page
    PRECONDITIONS: 2) There is at least one surface bet added to the SLP/Homepage in CMS.
    PRECONDITIONS: 3)There are other modules active and configured in CMS for this homepage/SLP
    PRECONDITIONS: 4)Open this SLP/Homepage in Oxygen application.
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_preconditionshomepageverify_the_order_of_the_surface_bet_module_in_homepage(self):
        """
        DESCRIPTION: Navigate to module from preconditions(Homepage),verify the order of the surface bet module in homepage.
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_login_to_oxygen_applicationverify_order_of_surfacebet_module_in_homepage(self):
        """
        DESCRIPTION: Login to oxygen application,Verify order of Surfacebet module in homepage
        EXPECTED: Oxygen app should launch successfully,Surfacebet module order should be same as CMS.
        """
        pass

    def test_004_change_the_module_order_in_the_cms_and_verify_in_fe(self):
        """
        DESCRIPTION: Change the module order in the CMS and verify in FE
        EXPECTED: The order is updated without refresh,module order should be same as CMS configurations
        """
        pass
