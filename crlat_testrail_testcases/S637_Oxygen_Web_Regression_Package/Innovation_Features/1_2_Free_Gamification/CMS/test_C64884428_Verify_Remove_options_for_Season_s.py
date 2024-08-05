import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C64884428_Verify_Remove_options_for_Season_s(Common):
    """
    TR_ID: C64884428
    NAME: Verify Remove options for Season/s
    DESCRIPTION: This test case verifies that User can Remove the existing Season/s
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: Season/s should be created and displayed in 1-2 Free
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_validate_the_display_of_1_2_free_tab_in_left_side_menu_of_cms(self):
        """
        DESCRIPTION: Validate the display of '1-2 Free' tab in left side menu of CMS
        EXPECTED: User should be able to view the '1-2 Free' tab
        """
        pass

    def test_003_click_on_1_2_free_tab(self):
        """
        DESCRIPTION: Click on '1-2 Free' tab
        EXPECTED: * User should be able to click on '1-2 Free' tab
        EXPECTED: * Sub Menu list of item/s should be displayed
        """
        pass

    def test_004_verify_display_of_seasons(self):
        """
        DESCRIPTION: Verify display of Seasons
        EXPECTED: Seasons should be displayed
        """
        pass

    def test_005_click_on_seasons_from_the_sub_menu(self):
        """
        DESCRIPTION: Click on Seasons from the sub menu
        EXPECTED: User should be navigate to Seasons page and the below fields should be displayed
        EXPECTED: ##When no Seasons are configured##
        EXPECTED: * Create Season
        EXPECTED: ##When at least one Season is configured##
        EXPECTED: * Create Season
        EXPECTED: * Table with below column Headers
        EXPECTED: * Season Name
        EXPECTED: * Start Date
        EXPECTED: * End Date
        EXPECTED: * Remove
        EXPECTED: * Edit
        EXPECTED: * Search bar should be available
        """
        pass

    def test_006_single_removalclick_on_remove_buttonmultiple_removalselect_the_check_boxes_for_more_than_one_contest_and_click_on_remove_button(self):
        """
        DESCRIPTION: **Single Removal**
        DESCRIPTION: Click on Remove button
        DESCRIPTION: **Multiple Removal**
        DESCRIPTION: Select the check boxes for more than one Contest and Click on Remove button
        EXPECTED: Confirmation Pop-up will be displayed with Yes and No options
        """
        pass

    def test_007_click_on_yes_and_verify(self):
        """
        DESCRIPTION: Click on Yes and Verify
        EXPECTED: User will be redirected to the same page with the Season removed
        EXPECTED: **If there is only one Season**
        EXPECTED: Table should no longer be displayed
        """
        pass

    def test_008_click_on_no_and_verify(self):
        """
        DESCRIPTION: Click on No and Verify
        EXPECTED: User will be redirected to the same page with the Season still displayed
        """
        pass

    def test_009_validate_drag__drop(self):
        """
        DESCRIPTION: Validate Drag & Drop
        EXPECTED: * User should be able to use the drag & drop to change the positions of the Season
        EXPECTED: **Page Refresh**
        EXPECTED: * User selected positions should remain unchanged
        """
        pass
