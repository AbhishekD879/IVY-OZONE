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
class Test_C64884429_Verify_Search_options_for_Season(Common):
    """
    TR_ID: C64884429
    NAME: Verify Search options for Season
    DESCRIPTION: This test case verifies that User search for the existing Season
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: Seasons sub menu should be configured in 1-2 Free
    PRECONDITIONS: 3: Season should be created and displayed in 1-2 Free
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_click_on_1_2_free_tab_in_left_side_menu_of_cms(self):
        """
        DESCRIPTION: Click on '1-2 Free' tab in left side menu of CMS
        EXPECTED: * User should be able to click on '1-2 Free' tab
        EXPECTED: * Sub Menu list of item/s should be displayed
        """
        pass

    def test_003_click_on_seasons_from_the_sub_menu(self):
        """
        DESCRIPTION: Click on Seasons from the sub menu
        EXPECTED: User should be navigate to Seasons page and the below fields should be displayed
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

    def test_004_verify_search_functionenter_season_name(self):
        """
        DESCRIPTION: Verify Search function
        DESCRIPTION: Enter Season name
        EXPECTED: Season name should be displayed at the top
        EXPECTED: **If there are more than one Season with same name**
        EXPECTED: Latest created Season will be displayed at the top
        """
        pass
