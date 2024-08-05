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
class Test_C63761122_Verify_Remove_Module_ribbon_tab_with_universalwith_single_exclusion_and_verify_in_FE(Common):
    """
    TR_ID: C63761122
    NAME: Verify Remove Module ribbon tab with universal(with single exclusion) and verify in FE
    DESCRIPTION: This test case verifies removal Universal (with single exclusion)
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Module ribbon tab
    PRECONDITIONS: 2) Create a Universal (with single  exclusion) Module ribbon tab
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

    def test_003_click_on_module_ribbon_tab_link(self):
        """
        DESCRIPTION: Click on Module ribbon tab link.
        EXPECTED: User should be able to view existing Module ribbon tabs should be displayed.
        """
        pass

    def test_004_click_on_existing_module_ribbon_tab_with_universal_with_single_exclusion(self):
        """
        DESCRIPTION: Click on existing Module ribbon tab with Universal (with single exclusion)
        EXPECTED: Module ribbon tab detail page should be opened  with Universal (with single exclusion)
        """
        pass

    def test_005_click_on_remove_button(self):
        """
        DESCRIPTION: Click on Remove button
        EXPECTED: Module ribbon tab should be removed successfully
        """
        pass

    def test_006_load_oxygen_and_verify_module_ribbon_tab(self):
        """
        DESCRIPTION: Load oxygen and verify Module ribbon tab
        EXPECTED: Removed Module ribbon tab should not be shown in application
        """
        pass
