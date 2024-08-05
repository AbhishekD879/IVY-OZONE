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
class Test_C63761097_Verify_search_functionality_on_displayed_Module_ribbon_tab_module_page(Common):
    """
    TR_ID: C63761097
    NAME: Verify search functionality on displayed Module ribbon tab module page.
    DESCRIPTION: This test case verifies search functionality by text in the records shown on the table in Module ribbon tab module page.
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Module ribbon tab
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        pass

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be able to view the Module ribbon tab Module page
        """
        pass

    def test_003_click_at_search_for_module_ribbon_tab(self):
        """
        DESCRIPTION: Click at "Search for Module ribbon tab"
        EXPECTED: User should able to click and able to enter text
        """
        pass

    def test_004_search_by_link_tittle(self):
        """
        DESCRIPTION: Search by link tittle
        EXPECTED: a) Should able to search by Link tittle, all related records should be shown
        EXPECTED: b) results should retain from selected drop down only which means if user select any segment search should not display Module ribbon tabs in other segment
        """
        pass
