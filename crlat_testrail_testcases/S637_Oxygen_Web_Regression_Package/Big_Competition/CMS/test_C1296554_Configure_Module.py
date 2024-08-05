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
class Test_C1296554_Configure_Module(Common):
    """
    TR_ID: C1296554
    NAME: Configure Module
    DESCRIPTION: This test case verifies the configuration of Module in CMS
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: * https://coral-cms-dev0.symphony-solutions.eu
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is loaded
        """
        pass

    def test_002_go_to_big_competition_section___choose_competition___choose_tab_that_has_inactive_subtabs_option(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has inactive SubTabs option
        EXPECTED: Tab landing page is opened
        """
        pass

    def test_003_create_a_few_different_modules(self):
        """
        DESCRIPTION: Create a few different Modules
        EXPECTED: Modules are created and disabled by default
        """
        pass

    def test_004_change_order_of_modules_by_drag_n_drop(self):
        """
        DESCRIPTION: Change order of Modules by drag-n-drop
        EXPECTED: Order is changed
        """
        pass

    def test_005_load_oxygen___check_order_of_modules_on_fe(self):
        """
        DESCRIPTION: Load Oxygen -> check order of Modules on FE
        EXPECTED: Order of Modules on FE corresponds to order configured on step #4
        """
        pass

    def test_006_in_cms_click_on_delete_icon_opposite_to_module_name_and_confirm_removing_it(self):
        """
        DESCRIPTION: In CMS click on 'delete' icon opposite to Module name and confirm removing it
        EXPECTED: * 'Remove Completed' success pop-up is displayed
        EXPECTED: * Module is no more displayed within the list of all Modules
        """
        pass

    def test_007_load_oxygen___check_module_existence_on_fe(self):
        """
        DESCRIPTION: Load Oxygen -> check Module existence on FE
        EXPECTED: Deleted on step #6 Module is NOT displayed on FE
        """
        pass

    def test_008_in_cms_go_to_module_details_page_and_change_the_module_name_field_and_save_changes(self):
        """
        DESCRIPTION: In CMS go to Module Details page and change the 'Module Name' field and save changes
        EXPECTED: * Changes are saved
        EXPECTED: * Name of Module is changed on FE
        """
        pass

    def test_009_make_some_changes_on_module_details_page_click_on_revert_changes_button_and_click_yes_option_on_revert_changes_pop_up(self):
        """
        DESCRIPTION: Make some changes on Module Details page, click on 'Revert Changes' button and click 'Yes' option on 'Revert Changes' pop-up
        EXPECTED: * Changes are reverted
        EXPECTED: * 'Save Changes' and 'Revert Changes' buttons are disabled
        """
        pass

    def test_010_make_some_changes_on_module_details_page_navigate_to_another_page_via_breadcrumbs_and_click_yes_on_leaving_pop_up(self):
        """
        DESCRIPTION: Make some changes on Module Details page, navigate to another page via breadcrumbs and click 'Yes' on 'Leaving' pop-up
        EXPECTED: * Changes on Module Details page are NOT saved
        EXPECTED: * User is navigated to the corresponding page
        EXPECTED: * 'Save Changes' and 'Revert Changes' buttons are disabled
        """
        pass

    def test_011_go_to_big_competition_section___choose_competition___choose_tab___choose_subtab___choose_a_module(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab -> choose SubTab -> choose a Module
        EXPECTED: 
        """
        pass

    def test_012_repeat_step_3_9(self):
        """
        DESCRIPTION: Repeat step #3-9
        EXPECTED: 
        """
        pass
