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
class Test_C62903985_Verify_on_successful_creation_page_should_navigate_to_the_Featured_tab_module_module_page(Common):
    """
    TR_ID: C62903985
    NAME: Verify on successful creation, page should navigate to the Featured tab module module page
    DESCRIPTION: This test case verifies page navigation after successful creation to the Featured tab module Module page
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Featured tab module
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_featured_tab_module_link_and_configure_one_featured_tab_module(self):
        """
        DESCRIPTION: click on Featured tab module link and configure one Featured tab module.
        EXPECTED: On successful creation, page should navigate to the Featured tab module Module page.
        """
        pass
