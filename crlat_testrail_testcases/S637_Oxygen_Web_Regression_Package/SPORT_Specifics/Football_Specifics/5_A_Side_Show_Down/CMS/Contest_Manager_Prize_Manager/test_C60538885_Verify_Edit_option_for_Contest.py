import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C60538885_Verify_Edit_option_for_Contest(Common):
    """
    TR_ID: C60538885
    NAME: Verify Edit option for Contest
    DESCRIPTION: This test case verifies that User can Edit the existing Contests
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: Contests should be created and displayed in CMS - 5-A Side Showdown
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_validate_the_display_of_5_a_side_showdown_tab_in_left_side_menu_of_cms(self):
        """
        DESCRIPTION: Validate the display of '5-A Side showdown' tab in left side menu of CMS
        EXPECTED: User should be able to view the 5-A Side showdown tab
        """
        pass

    def test_003_click_on_5_a_side_showdown_tab(self):
        """
        DESCRIPTION: Click on '5-A Side showdown' tab
        EXPECTED: User should be navigate to Contest page and the below should be displayed
        EXPECTED: ##When no Contests are configured##
        EXPECTED: * Add New Contest
        EXPECTED: ##When at least one Contest is configured##
        EXPECTED: * Add New Contest
        EXPECTED: * Table with below column Headers
        EXPECTED: * Contest Name
        EXPECTED: * Date - Event Start Date
        EXPECTED: * Active
        EXPECTED: * Remove
        EXPECTED: * Edit
        EXPECTED: * Table should include a drag and drop before the Contest name
        EXPECTED: * Search bar should be available
        """
        pass

    def test_004_click_on_edit_button(self):
        """
        DESCRIPTION: Click on Edit button
        EXPECTED: User should be redirected to Edit Contest Details page
        """
        pass

    def test_005_verify_after_making_changes_in_the_contest_details(self):
        """
        DESCRIPTION: Verify after making changes in the Contest details
        EXPECTED: User should be able to save the changes successfully
        """
        pass

    def test_006_validate_drag__drop(self):
        """
        DESCRIPTION: Validate Drag & Drop
        EXPECTED: * User should be able to use the drag & drop to change the positions of the contest
        EXPECTED: **Page Refresh**
        EXPECTED: * User selected positions should remain unchanged
        """
        pass
