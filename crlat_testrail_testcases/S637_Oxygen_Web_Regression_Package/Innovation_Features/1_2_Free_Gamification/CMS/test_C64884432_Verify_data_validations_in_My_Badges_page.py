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
class Test_C64884432_Verify_data_validations_in_My_Badges_page(Common):
    """
    TR_ID: C64884432
    NAME: Verify data validations in My Badges page
    DESCRIPTION: This test case verifies data validations in My Badges page
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2:My Badges menu should be configured in 1-2 Free
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

    def test_004_validate_the_display_of_my_badges_in_sub_menu_list_of_items(self):
        """
        DESCRIPTION: Validate the display of 'My Badges' in Sub Menu list of item/s
        EXPECTED: User should be able to view My Badges
        """
        pass

    def test_005_click_on_my_badges_from_the_sub_menu(self):
        """
        DESCRIPTION: Click on My Badges from the sub menu
        EXPECTED: User should be navigate to MY Badges page and the below fields should be displayed
        EXPECTED: * My Badges Label
        EXPECTED: * Rules Display
        EXPECTED: * Display Last Update Date & Time
        EXPECTED: * Save Changes
        EXPECTED: * Revert Changes
        """
        pass

    def test_006_verify_the_data_validations_of_the_fields(self):
        """
        DESCRIPTION: Verify the data validations of the fields
        EXPECTED: * My Badges Label - Textbox (Allow to enter 50 characters)
        EXPECTED: * Rules Display - Textbox (Allow to enter 200 characters)
        EXPECTED: * Display Last Update Date & Time - Checkbox (Check/Uncheck)
        """
        pass
