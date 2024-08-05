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
class Test_C64884434_Verify_Edit_option_for_Season(Common):
    """
    TR_ID: C64884434
    NAME: Verify Edit option for Season
    DESCRIPTION: This test case verifies that User can Edit the existing Season
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: Season should be created and displayed in CMS - 1-2 Free -&gt; Seasons
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_validate_the_display_of_seasons_sub_menu_in_1_2_free(self):
        """
        DESCRIPTION: Validate the display of 'Seasons' Sub Menu in 1-2 Free
        EXPECTED: User should be able to view the Seasons Sub Menu
        """
        pass

    def test_003_click_on_seasons_sub_menu(self):
        """
        DESCRIPTION: Click on 'Seasons' sub menu
        EXPECTED: User should be navigate to seasons page and the below should be displayed
        EXPECTED: ##When at least one Contest is configured##
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

    def test_004_click_on_edit_button_on_specific_season(self):
        """
        DESCRIPTION: Click on Edit button on specific season
        EXPECTED: User should be redirected to Edit season Details page
        """
        pass

    def test_005_verify_after_making_changes_in_the_season_details(self):
        """
        DESCRIPTION: Verify after making changes in the season details
        EXPECTED: User should be able to save the changes successfully
        """
        pass

    def test_006_validate_drag__drop(self):
        """
        DESCRIPTION: Validate Drag & Drop
        EXPECTED: * User should be able to use the drag & drop to change the positions of the season
        EXPECTED: **Page Refresh**
        EXPECTED: * User selected positions should remain unchanged
        """
        pass
