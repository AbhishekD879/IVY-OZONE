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
class Test_C61618992_Verify_Edit_Prizes_in_Pay_Table(Common):
    """
    TR_ID: C61618992
    NAME: Verify Edit  Prizes in Pay Table
    DESCRIPTION: This test case verifies that CMS user can Edit individual prizes directly from the pay table
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: Contest should be created and Prizes are added
    PRECONDITIONS: ***How to Configure Menu Item***
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    """
    keep_browser_open = True

    def test_001_login_as_cms_admin_user(self):
        """
        DESCRIPTION: Login as CMS admin User
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_click_on_5_a_side_showdown_tab(self):
        """
        DESCRIPTION: Click on '5-A Side showdown' tab
        EXPECTED: User should be navigate to Contest page and the below should be displayed
        EXPECTED: ##When no Contests are configured##
        EXPECTED: * Add New Contest
        EXPECTED: ##When at least one Contest is configured##
        EXPECTED: * Add New Contest
        EXPECTED: * Table with below column Headers
        EXPECTED: * Contest Name
        EXPECTED: * Date
        EXPECTED: * Active
        EXPECTED: * Remove
        EXPECTED: * Edit
        EXPECTED: * Table should include a drag and drop before the Contest name
        EXPECTED: * Search bar should be available
        """
        pass

    def test_003_click_on_edit_button(self):
        """
        DESCRIPTION: Click on Edit button
        EXPECTED: User should be navigated to  Contest Edit Details page
        """
        pass

    def test_004__scroll_down_to_add_a_prize_section_click_on_edit_button_for_any_individual_prize_entry(self):
        """
        DESCRIPTION: * Scroll down to Add A Prize section
        DESCRIPTION: * Click on Edit button for any Individual Prize entry
        EXPECTED: * User should be redirected to Edit Prize
        """
        pass

    def test_005_verify_after_making_changes_in_prize_entry(self):
        """
        DESCRIPTION: Verify after making changes in prize entry
        EXPECTED: * User should be able to save the changes successfully
        """
        pass
