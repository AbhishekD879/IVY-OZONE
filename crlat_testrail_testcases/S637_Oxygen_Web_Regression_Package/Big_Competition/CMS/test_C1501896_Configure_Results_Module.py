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
class Test_C1501896_Configure_Results_Module(Common):
    """
    TR_ID: C1501896
    NAME: Configure 'Results' Module
    DESCRIPTION: Current test case describes how to create and configure Results module
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: https://coral-cms-dev1.symphony-solutions.eu - Phoenix env
    PRECONDITIONS: https://coral-cms-dev0.symphony-solutions.eu - Develop
    PRECONDITIONS: Big Competition is created:
    PRECONDITIONS: - Competition type ID it must be valid - please note that it should be a competition that has any result (not future)
    """
    keep_browser_open = True

    def test_001_load_cms_and_log_in(self):
        """
        DESCRIPTION: Load CMS and log in
        EXPECTED: CMS is loaded
        EXPECTED: User is logged in
        """
        pass

    def test_002_go_to_big_competition_section___choose_competition___choose_tab_that_has_subtabs_option__choose_a_sub_tab(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has SubTabs option > choose a Sub-tab
        EXPECTED: Sub-tab landing page is opened
        """
        pass

    def test_003_create_new_results_module_type(self):
        """
        DESCRIPTION: Create new Results module type
        EXPECTED: New module with 'Results' type is created
        EXPECTED: New module is disabled by default
        """
        pass

    def test_004_click_on_results_module_name(self):
        """
        DESCRIPTION: Click on Results module name
        EXPECTED: Module details page is loaded
        """
        pass

    def test_005_verify_results_module_details_page(self):
        """
        DESCRIPTION: Verify Results Module details page
        EXPECTED: Active' checkbox is unchecked
        EXPECTED: 'Module Name' (mandatory) field. Entered when the module was created
        EXPECTED: 'Module Type' (disabled) field is filled out by selected type value - 'RESULTS' in our case
        EXPECTED: 'Max Display' mandatory input field is present (7 is a default value)
        EXPECTED: 'Available Seasons' dropdown list is present (empty by default)
        EXPECTED: 'Save Changes', 'Revert Changes' and 'Remove' buttons are present and disabled by default
        """
        pass

    def test_006_check_active_checkbox_set_a_value_to_available_seasons_change_module_name_and_press_save_changes(self):
        """
        DESCRIPTION: Check 'Active' checkbox, set a value to 'Available Seasons', change module name and press 'Save Changes'
        EXPECTED: Observe that 'Save Changes' only becomes active upon all mandatory fields are filled
        EXPECTED: 'Are You Sure You Want to Save This: 'new module name'?' popup is displayed
        """
        pass

    def test_007_press_yes_and_then_ok_button(self):
        """
        DESCRIPTION: Press 'Yes' and then 'Ok' button
        EXPECTED: 'Competition Module is Successfully Saved' popup is displayed
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_008_enter_0_into_max_display_input_field(self):
        """
        DESCRIPTION: Enter 0 into 'Max Display' input field
        EXPECTED: 'Max display should be entered' red error is displayed
        """
        pass

    def test_009_set_any_number_using_arrows_at_the_end_of_max_display_input_field_try_up_and_down(self):
        """
        DESCRIPTION: Set any number using arrows at the end of 'Max Display input field' (Try up and down)
        EXPECTED: Value is changed successfully
        """
        pass

    def test_010_press_save_changes___yes___and_ok_buttons(self):
        """
        DESCRIPTION: Press 'Save Changes' -> 'Yes' -> and 'Ok' buttons
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_011_open_max_display_dropdown_list(self):
        """
        DESCRIPTION: Open 'Max Display' dropdown list
        EXPECTED: List of all available seasons for current competition is present
        EXPECTED: You can check this in response:
        EXPECTED: ![](index.php?/attachments/get/20526)
        """
        pass

    def test_012_select_any_season_and_press_save_changes___yes___and_ok_buttons(self):
        """
        DESCRIPTION: Select any season and press 'Save Changes' -> 'Yes' -> and 'Ok' buttons
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_013_go_to_big_competition_section___choose_competition___choose_tab_that_has_no_subtabs_option_set(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has no SubTabs option set
        EXPECTED: Tab landing page is opened
        """
        pass

    def test_014_repeat_steps_3___12(self):
        """
        DESCRIPTION: Repeat Steps 3 - 12
        EXPECTED: Results are the same
        """
        pass

    def test_015_press_remove_button(self):
        """
        DESCRIPTION: Press 'Remove' button
        EXPECTED: 'Are You Sure You Want to Remove : 'module name'?' popup is displayed
        """
        pass

    def test_016_press_yes_button(self):
        """
        DESCRIPTION: Press 'Yes' button
        EXPECTED: User is redirected to the Tab landing page
        EXPECTED: The module is not present in the list
        """
        pass
