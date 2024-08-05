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
class Test_C62701144_Verify_search_functionality_on_displayed_super_button_module_page(Common):
    """
    TR_ID: C62701144
    NAME: Verify search functionality on displayed super button module page.
    DESCRIPTION: This test case verifies search functionality by text in the records shown on the table in super button module page.
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button.
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
        EXPECTED: User should be able to view the Super button Module page
        """
        pass

    def test_003_click_at_search_for_super_button(self):
        """
        DESCRIPTION: Click at "Search for super button"
        EXPECTED: User should able to click and able to enter text
        """
        pass

    def test_004_search_by_link_tittle(self):
        """
        DESCRIPTION: Search by link tittle
        EXPECTED: a) Should able to search by Link tittle, all related records should be shown
        EXPECTED: b) results should retain from selected drop down only which means if user select any segment search should not display super buttons in other segment
        """
        pass
