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
class Test_C1500090_Add_Configure_Promotions_Module(Common):
    """
    TR_ID: C1500090
    NAME: Add/Configure 'Promotions' Module
    DESCRIPTION: 
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: https://coral-cms-dev1.symphony-solutions.eu - Phoenix env
    PRECONDITIONS: https://coral-cms-dev0.symphony-solutions.eu - Develop
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
        EXPECTED: Sub-Tab landing page is opened
        """
        pass

    def test_003_create_new_promotions_module_type(self):
        """
        DESCRIPTION: Create new Promotions module type
        EXPECTED: New module with 'Promotions' type is created
        EXPECTED: New module is disabled by default
        """
        pass

    def test_004_click_on_promotions_module_name(self):
        """
        DESCRIPTION: Click on Promotions module name
        EXPECTED: Module details page is loaded
        """
        pass

    def test_005_verify_promotions_module_details_page(self):
        """
        DESCRIPTION: Verify Promotions Module details page
        EXPECTED: Active' checkbox is unchecked
        EXPECTED: 'Module Name' (mandatory) field. Entered when the module was created
        EXPECTED: 'Module Type' (disabled) field is filled out by selected type value - 'Promotions' in our case
        EXPECTED: 'No additional configurations available' message is present
        EXPECTED: 'Save Changes', 'Revert Changes' and 'Remove' buttons are present and disabled by default
        """
        pass

    def test_006_check_active_checkbox_and_press_save_changes_button(self):
        """
        DESCRIPTION: Check 'Active' checkbox and press 'Save Changes' button
        EXPECTED: 'Are You Sure You Want to Save This: qwerty?' popup is displayed
        """
        pass

    def test_007_press_yes_and_then_ok_button(self):
        """
        DESCRIPTION: Press 'Yes' and then 'Ok' button
        EXPECTED: 'Competition Module is Successfully Saved' popup is displayed
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_008_go_to_big_competition_section___choose_competition___choose_tab_that_has_no_subtabs_option_set(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has no SubTabs option set
        EXPECTED: Tab landing page is opened
        """
        pass

    def test_009_repeat_steps_3___7(self):
        """
        DESCRIPTION: Repeat Steps 3 - 7
        EXPECTED: Results are the same
        """
        pass

    def test_010_press_remove_button(self):
        """
        DESCRIPTION: Press 'Remove' button
        EXPECTED: 'Are You Sure You Want to Remove : 'module name'?' popup is displayed
        """
        pass

    def test_011_press_yes_button(self):
        """
        DESCRIPTION: Press 'Yes' button
        EXPECTED: User is redirected to the Tab landing page
        EXPECTED: The module is not present in the list
        """
        pass
