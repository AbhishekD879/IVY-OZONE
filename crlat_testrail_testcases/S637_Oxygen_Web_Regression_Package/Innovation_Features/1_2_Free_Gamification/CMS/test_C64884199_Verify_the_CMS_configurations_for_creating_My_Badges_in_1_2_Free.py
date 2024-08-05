import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C64884199_Verify_the_CMS_configurations_for_creating_My_Badges_in_1_2_Free(Common):
    """
    TR_ID: C64884199
    NAME: Verify the CMS configurations for creating My Badges in 1-2 Free
    DESCRIPTION: This test case verifies CMS configurations for creating My Badges in 1-2 Free
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: Free Ride menu should be configured in CMS
    PRECONDITIONS: ***How to Configure Sub Menu Item***
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: My Badges
    PRECONDITIONS: Path: /My Badges
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_click_on_1_2_free_tab(self):
        """
        DESCRIPTION: Click on '1-2 Free' tab
        EXPECTED: * User should be able to click on '1-2 Free' tab
        EXPECTED: * Sub Menu list of item/s should be displayed
        """
        pass

    def test_003_validate_the_display_of_my_badges_in_sub_menu_list_of_items(self):
        """
        DESCRIPTION: Validate the display of 'My Badges' in Sub Menu list of item/s
        EXPECTED: User should be able to view My Badges
        """
        pass

    def test_004_click_on_my_badges_from_the_sub_menu(self):
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

    def test_005_enter_data_in_the_above_fields(self):
        """
        DESCRIPTION: Enter data in the above fields
        EXPECTED: * User should be able to enter the details in My Badges Label and Rules Display fields
        EXPECTED: * User should be able to check/uncheck in Display Last Update Date & Time field
        """
        pass

    def test_006_click_on_save_changes(self):
        """
        DESCRIPTION: Click on Save Changes
        EXPECTED: * My Badges should be created successfully
        """
        pass

    def test_007_modify_the_existing_my_badges_data_in_below_fields_my_badges_label_rules_display_display_last_update_date__time(self):
        """
        DESCRIPTION: Modify the existing My Badges data in below fields
        DESCRIPTION: * My Badges Label
        DESCRIPTION: * Rules Display
        DESCRIPTION: * Display Last Update Date & Time
        EXPECTED: Modified data should be reflected
        """
        pass

    def test_008_verify_the_state_of_revert_button(self):
        """
        DESCRIPTION: Verify the state of 'Revert' Button
        EXPECTED: 'Revert' Button should be in enabled state
        """
        pass

    def test_009_click_on_revert_button(self):
        """
        DESCRIPTION: Click on 'Revert' Button
        EXPECTED: Modified data fields should reflect with the previously saved data
        """
        pass
