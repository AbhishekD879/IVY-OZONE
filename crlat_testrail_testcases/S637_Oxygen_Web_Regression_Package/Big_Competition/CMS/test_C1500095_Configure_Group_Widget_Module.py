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
class Test_C1500095_Configure_Group_Widget_Module(Common):
    """
    TR_ID: C1500095
    NAME: Configure 'Group Widget' Module
    DESCRIPTION: This test case verifies configuration of 'Groups Widget' Module
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: * https://coral-cms-dev1.symphony-solutions.eu - Phoenix env
    PRECONDITIONS: * https://coral-cms-dev0.symphony-solutions.eu - Develop
    """
    keep_browser_open = True

    def test_001_load_cms_and_log_in(self):
        """
        DESCRIPTION: Load CMS and log in
        EXPECTED: * CMS is loaded
        EXPECTED: * User is logged in
        """
        pass

    def test_002_go_to_big_competition_section___choose_competition___choose_tab_that_has_subtabs_option_eg_groups__choose_a_sub_tab(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has SubTabs option (e.g. Groups) > choose a Sub-tab
        EXPECTED: Sub-Tab landing page is opened
        """
        pass

    def test_003_create_new_module_with_group_widget_type(self):
        """
        DESCRIPTION: Create new Module with 'Group Widget' type
        EXPECTED: * New module with 'Group Widget' type is created
        EXPECTED: * New module is disabled by default
        """
        pass

    def test_004_go_to_module_details_page_from_step_3(self):
        """
        DESCRIPTION: Go to Module details page (from Step 3)
        EXPECTED: Module details page is loaded
        """
        pass

    def test_005_verify_default_controls_on_module_details_page(self):
        """
        DESCRIPTION: Verify default controls on Module details page
        EXPECTED: * 'Active' check box is unchecked
        EXPECTED: * 'Module Name' (mandatory) field is filled out by set name of the module
        EXPECTED: * 'Module Type' (disabled) field is filled out by selected type value  - 'GROUP_WIDGET'
        EXPECTED: * 'Qualified teams' selector, default value is 0
        EXPECTED: * 'Available Seasons' selector with the list of available seasons
        EXPECTED: * 'Group name'  and ''Redirect link paths' tab
        EXPECTED: * 'Available Groups' and a drop-down list with all available valid URL of respective Big Competition
        EXPECTED: * 'Save Changes', 'Revert Changes' and 'Remove' buttons
        """
        pass

    def test_006_attempt_to_save_with_any_of_the_mandatory_fields_left_blank_module_name_qualified_teams_available_seasons_redirect_link_paths(self):
        """
        DESCRIPTION: Attempt to 'Save' with any of the mandatory fields left blank:
        DESCRIPTION: * Module Name
        DESCRIPTION: * Qualified teams
        DESCRIPTION: * Available Seasons
        DESCRIPTION: * Redirect link paths
        EXPECTED: * It is not possible to save with any of the mandatory fields left blank
        EXPECTED: * 'Save' button is disabled
        """
        pass

    def test_007_set_active_check_box_qualified_teams_available_seasons_redirect_link_paths_tap_save_changes(self):
        """
        DESCRIPTION: Set:
        DESCRIPTION: * 'Active' check box
        DESCRIPTION: * 'Qualified Teams'
        DESCRIPTION: * 'Available Seasons'
        DESCRIPTION: * 'Redirect link paths'
        DESCRIPTION: > Tap 'Save Changes'
        EXPECTED: * Success pop-up is displayed
        """
        pass

    def test_008_go_to_big_competition_section___choose_competition___choose_tab_that_has_no_subtabs_option_set(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has no SubTabs option set
        EXPECTED: Tab landing page is opened
        """
        pass

    def test_009_repeat_steps_2___8(self):
        """
        DESCRIPTION: Repeat Steps 2 - 8
        EXPECTED: 
        """
        pass
