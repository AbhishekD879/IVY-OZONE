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
class Test_C62701146_Verify_super_buttons_display_as_per_selected_segment_from_drop_down_list(Common):
    """
    TR_ID: C62701146
    NAME: Verify super buttons display as per selected segment from drop down list
    DESCRIPTION: This test case verifies segment dropdown functionality on super button module page.
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button.
    PRECONDITIONS: 2) Should have super buttons for specific user
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
        EXPECTED: User should be able to view the super button Module page
        """
        pass

    def test_003_verify_super_button_page(self):
        """
        DESCRIPTION: Verify super button page
        EXPECTED: The super button Module page as per the designs below
        EXPECTED: Create super button
        EXPECTED: Segment
        EXPECTED: Download CSV
        EXPECTED: Search field
        """
        pass

    def test_004_verify_segment_dropdown_by_selecting_specific_segment(self):
        """
        DESCRIPTION: Verify Segment dropdown by selecting specific segment
        EXPECTED: The dropdown will show segmented records
        EXPECTED: Note: When user is performing search, how we are going to display the table- Search operation will basically return search result from the segment data which is selected in segment dropdown.
        """
        pass
