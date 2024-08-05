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
class Test_C1503904_Configure_Groups_All_Module(Common):
    """
    TR_ID: C1503904
    NAME: Configure 'Groups All' Module
    DESCRIPTION: This test case verifies the configuration of 'Groups All' Module
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: https://coral-cms-dev1.symphony-solutions.eu - Phoenix env
    PRECONDITIONS: https://coral-cms-dev0.symphony-solutions.eu - Develop
    """
    keep_browser_open = True

    def test_001_load_cms_and_log_in(self):
        """
        DESCRIPTION: Load CMS and log in
        EXPECTED: - CMS is loaded
        EXPECTED: - User is logged in
        """
        pass

    def test_002_go_to_big_competition_section___choose_competition___choose_tab_that_has_subtabs_option_eg_groups__choose_a_sub_tab(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has SubTabs option (e.g. Groups) > choose a Sub-tab
        EXPECTED: Sub-Tab landing page is opened
        """
        pass

    def test_003_create_new_module_with_group_all_type(self):
        """
        DESCRIPTION: Create new Module with 'Group All' type
        EXPECTED: - New module with 'Group All' type is created
        EXPECTED: - New module is disabled by default
        """
        pass

    def test_004_go_to_module_details_page(self):
        """
        DESCRIPTION: Go to Module details page
        EXPECTED: Module details page is loaded
        """
        pass

    def test_005_verify_default_controls_on_module_details_page(self):
        """
        DESCRIPTION: Verify default controls on Module details page
        EXPECTED: 'Active' check box is unchecked
        EXPECTED: 'Module Name' (mandatory) field is filled out by set name of the module
        EXPECTED: 'Module Type' (disabled) field is filled out by selected type value- 'GROUP_ALL'
        EXPECTED: 'Qualified teams' selector, default value is 0
        EXPECTED: 'Available Groups' selector with the list of available Groups for current competition (e.g. World Cup, Group A; World Cup, Group B) > should be retrieved from OB or Stats center
        EXPECTED: 'Available Seasons' selector (mandatory for Group Individual) with the list of available seasons
        EXPECTED: 'Add Outrught Market ID' area:
        EXPECTED: - 'Outright Market ID' selector
        EXPECTED: - 'Upload Market ID' button
        EXPECTED: - 'Loaded Outright Markets from OpenBet' grid ('No Outright Market's ID's Found' string is displayed, when no markets are available)
        EXPECTED: - 'Remove All' button
        EXPECTED: - 'Remove market red icon' (whae market is added)
        EXPECTED: 'Save Channges', 'Revert Changes' and 'Remove' buttons
        """
        pass

    def test_006_set_active_check_box_qualified_teams_available_groups_available_seasonspress_save_changes(self):
        """
        DESCRIPTION: Set:
        DESCRIPTION: * 'Active' check box
        DESCRIPTION: * 'Qualified Teams'
        DESCRIPTION: * 'Available Groups'
        DESCRIPTION: * 'Available Seasons'
        DESCRIPTION: Press 'Save Changes'
        EXPECTED: Success pop-up is displayed
        EXPECTED: Module is active, 'Qualified Teams', 'Available Groups', 'Available Seasons' are loaded into Module
        """
        pass

    def test_007_scroll_down_to_the_loaded_outright_markets_from_openbet_area(self):
        """
        DESCRIPTION: Scroll down to the 'Loaded Outright Markets from OpenBet' area
        EXPECTED: 
        """
        pass

    def test_008_enter_invalid_market_id_into_outright_market_id_selector_and_press_upload_market_id_button(self):
        """
        DESCRIPTION: Enter invalid market id into 'Outright Market ID' selector and press 'Upload Market ID' button
        EXPECTED: Red error message is displayed -'Outright Market ID is not valid. Try again.'
        """
        pass

    def test_009_enter_market_id_that_is_un_disabled_in_backoffice_into_outright_market_id_selector_and_press_upload_market_id_button(self):
        """
        DESCRIPTION: Enter market id that is un-disabled in backoffice into 'Outright Market ID' selector and press 'Upload Market ID' button
        EXPECTED: Red error message is displayed -'Outright Market ID is not valid. Try again.'
        """
        pass

    def test_010_enter_correct_market_id_into_outright_market_id_selector_and_press_upload_market_id_button(self):
        """
        DESCRIPTION: Enter correct market id into 'Outright Market ID' selector and press 'Upload Market ID' button
        EXPECTED: Market ID and market name is displayed on  'Loaded Outright Markets from OpenBet' grid
        EXPECTED: 'Openbet outright market is loaded!!' popup is displayed
        """
        pass

    def test_011_enter_that_same_market_id_from_step_9_and_press_upload_market_id_button(self):
        """
        DESCRIPTION: Enter that same market id (from step 9) and press 'Upload Market ID' button
        EXPECTED: Red error message is displayed - 'Outright Market ID already exists in markets id`s list.'
        """
        pass

    def test_012_enter_new_market_id_into_outright_market_id_selector_and_press_upload_market_id_button(self):
        """
        DESCRIPTION: Enter new market id into 'Outright Market ID' selector and press 'Upload Market ID' button
        EXPECTED: Market ID and market name is displayed on  'Loaded Outright Markets from OpenBet' grid
        EXPECTED: 'Openbet outright market is loaded!!' popup is displayed
        """
        pass

    def test_013_try_to_upload_the_third_market_id(self):
        """
        DESCRIPTION: Try to upload the third market id
        EXPECTED: Red error message is displayed - 'Outright Market ID`s quantitative should be not more than 2.'
        """
        pass

    def test_014_press_save_changes_button(self):
        """
        DESCRIPTION: Press 'Save Changes' button
        EXPECTED: Success pop-up is displayed
        EXPECTED: Markets are displayed on Module details page
        """
        pass

    def test_015_click_on_red_icon_next_to_market_id(self):
        """
        DESCRIPTION: Click on red icon next to market id
        EXPECTED: Marked removed successfully
        EXPECTED: 'OUTRIGHT MARKET Match Betting HAS BEEN REMOVED!!' popup is displayed
        """
        pass

    def test_016_go_to_big_competition_section___choose_competition___choose_tab_that_has_no_subtabs_option_set(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has no SubTabs option set
        EXPECTED: Tab landing page is opened
        """
        pass

    def test_017_repeat_steps_3___15(self):
        """
        DESCRIPTION: Repeat Steps 3 - 15
        EXPECTED: Results are the same
        """
        pass

    def test_018_press_remove_button(self):
        """
        DESCRIPTION: Press 'Remove' button
        EXPECTED: 'Are You Sure You Want to Remove : 'module name'?' popup is displayed
        """
        pass

    def test_019_press_yes_button(self):
        """
        DESCRIPTION: Press 'Yes' button
        EXPECTED: User is redirected to the Tab landing page
        EXPECTED: The module is not present in the list
        """
        pass
