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
class Test_C63761099_Verify_Module_ribbon_tabs_display_as_per_selected_segment_from_drop_down_list(Common):
    """
    TR_ID: C63761099
    NAME: Verify Module ribbon tabs display as per selected segment from drop down list
    DESCRIPTION: This test case verifies segment dropdown functionality on Module ribbon tab module page.
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Module ribbon tab
    PRECONDITIONS: 2) Should have Module ribbon tabs for specific user
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
        EXPECTED: User should be able to view the Module ribbon tab Module page
        """
        pass

    def test_003_verify_module_ribbon_tab_page(self):
        """
        DESCRIPTION: Verify Module ribbon tab page
        EXPECTED: The Module ribbon tab Module page as per the designs below
        EXPECTED: Create Module ribbon tab
        EXPECTED: Segment
        EXPECTED: Download CSV
        EXPECTED: Search field
        """
        pass

    def test_004_verify_segment_dropdown_by_selecting_specific_segment(self):
        """
        DESCRIPTION: Verify Segment dropdown by selecting specific segment
        EXPECTED: The dropdown will show segmented records
        EXPECTED: Note- When user is performing search, how we are going to display the table- Search operation will basically return search result from the segment data which is selected in segment dropdown.
        """
        pass
