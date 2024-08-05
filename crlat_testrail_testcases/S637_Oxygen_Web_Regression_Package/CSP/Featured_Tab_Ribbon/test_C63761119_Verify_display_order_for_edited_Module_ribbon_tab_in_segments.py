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
class Test_C63761119_Verify_display_order_for_edited_Module_ribbon_tab_in_segments(Common):
    """
    TR_ID: C63761119
    NAME: Verify display order for edited Module ribbon tab in segments
    DESCRIPTION: This test case verifies display order for edited Module ribbon tab in segments
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Module ribbon tab
    PRECONDITIONS: 2) Create a Segment(s) inclusion Module ribbon tab
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

    def test_004_click_on_existing_module_ribbon_tab_with_segment_inclusion(self):
        """
        DESCRIPTION: Click on existing Module ribbon tab with segment inclusion
        EXPECTED: Module ribbon tab detail page should be opened  with Segment(s)  inclusion radio button and segment(s) inclusion text box
        """
        pass

    def test_005_edit_existing_module_ribbon_tab(self):
        """
        DESCRIPTION: Edit existing Module ribbon tab
        EXPECTED: Add more than one segments in segment(s) inclusion text box
        """
        pass

    def test_006_click_on_save_changes_button(self):
        """
        DESCRIPTION: Click on save changes button
        EXPECTED: Module ribbon tab should be update successfully. Should navigate to Module ribbon tab module page
        """
        pass

    def test_007_verify_display_order_for_existing_and_newly_added_segment(self):
        """
        DESCRIPTION: Verify display order for existing and newly added segment
        EXPECTED: Segment belonged to existing before being edited, and the change was to newly add segment, the display order should not change for existing segments, but the configuration should display at the bottom of the list for newly added segment.
        """
        pass
