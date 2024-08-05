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
class Test_C1437223_Configure_Groups_Individual_Module(Common):
    """
    TR_ID: C1437223
    NAME: Configure 'Groups Individual' Module
    DESCRIPTION: This test case verifies configuration of 'Groups Individual' Module
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

    def test_003_create_new_module_with_group_individual_type(self):
        """
        DESCRIPTION: Create new Module with 'Group Individual' type
        EXPECTED: * New module with 'Group Individual' type is created
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
        EXPECTED: * 'Module Type' (disabled) field is filled out by selected type value 'GROUP_INDIVIDUAL'
        EXPECTED: * 'Qualified teams' selector, default value is 0
        EXPECTED: * 'Available Groups' selector (mandatory for Group Individual) with the list of available Groups for current competition (e.g. World Cup, Group A; World Cup, Group B) > should be retrieved from OB or Stats center
        EXPECTED: * 'Available Seasons' selector (mandatory for Group Individual) with the list of available seasons
        """
        pass

    def test_006_set_active_check_box_qualified_teams_available_groups_available_seasons_tap_save_changes(self):
        """
        DESCRIPTION: Set:
        DESCRIPTION: * 'Active' check box
        DESCRIPTION: * 'Qualified Teams'
        DESCRIPTION: * 'Available Groups'
        DESCRIPTION: * 'Available Seasons'
        DESCRIPTION: > Tap 'Save Changes'
        EXPECTED: * Success pop-up is displayed
        EXPECTED: * Module is active, 'Qualified Teams', 'Available Groups', 'Available Seasons' are loaded into Module
        """
        pass

    def test_007_go_to_big_competition_section___choose_competition___choose_tab_that_has_no_subtabs_option_set(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has no SubTabs option set
        EXPECTED: Tab landing page is opened
        """
        pass

    def test_008_repeat_steps_2___6(self):
        """
        DESCRIPTION: Repeat Steps 2 - 6
        EXPECTED: Results are the same
        """
        pass
