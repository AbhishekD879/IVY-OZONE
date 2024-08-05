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
class Test_C64881026_Verify_module_order_in_home_page(Common):
    """
    TR_ID: C64881026
    NAME: Verify module order in home page
    DESCRIPTION: This test case verifies module order in homepage
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page
    PRECONDITIONS: 2) There is atleast one record for all modules in Homepage
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_preconditionshomepageverify_the_order_of_all_modules_in_homepage(self):
        """
        DESCRIPTION: Navigate to module from preconditions(Homepage),verify the order of all modules in homepage.
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_login_to_oxygen_applicationverify_order_of_the_module_in_homepage(self):
        """
        DESCRIPTION: Login to oxygen application,Verify order of the module in homepage
        EXPECTED: Oxygen app should launch successfully,all modules order should be same as CMS.
        """
        pass

    def test_004_change_the_module_order_in_the_cms_and_verify_in_fe(self):
        """
        DESCRIPTION: Change the module order in the CMS and verify in FE
        EXPECTED: The order is updated without refresh,module order should be same as CMS configurations
        """
        pass
