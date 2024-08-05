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
class Test_C1288421_Configure_SubTab(Common):
    """
    TR_ID: C1288421
    NAME: Configure SubTab
    DESCRIPTION: This test case verifies configuration of SubTab in CMS
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

    def test_002_go_to_big_competition_section___choose_competition___choose_tab_which_has_tab_has_subtabs_option_set(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab which has 'Tab has SubTabs' option set
        EXPECTED: Tab landing page is opened
        """
        pass

    def test_003_create_a_few_different_subtabs_active_by_default(self):
        """
        DESCRIPTION: Create a few different SubTabs active by default
        EXPECTED: SubTabs are created and active
        """
        pass

    def test_004_change_order_of_subtabs_by_drag_n_drop(self):
        """
        DESCRIPTION: Change order of SubTabs by drag-n-drop
        EXPECTED: Order is changed
        """
        pass

    def test_005_load_oxygen___check_order_of_subtabs_on_fe(self):
        """
        DESCRIPTION: Load Oxygen -> check order of SubTabs on FE
        EXPECTED: Order of SubTabs on FE corresponds to order configured on step #4
        """
        pass

    def test_006_in_cms_click_on_delete_icon_opposite_to_subtab_name_and_confirm_removing_it(self):
        """
        DESCRIPTION: In CMS click on 'delete' icon opposite to SubTab name and confirm removing it
        EXPECTED: * 'Remove Completed' success pop-up is displayed
        EXPECTED: * SubTab is no more displayed within the list of all SubTabs
        """
        pass

    def test_007_load_oxygen___check_subtab_existence_on_fe(self):
        """
        DESCRIPTION: Load Oxygen -> check SubTab existence on FE
        EXPECTED: Deleted on step #6 SubTab is NOT displayed on FE
        """
        pass

    def test_008_in_cms_go_to_subtab_details_page_and_change_the_sub_tab_name_field_and_save_changes(self):
        """
        DESCRIPTION: In CMS go to SubTab Details page and change the 'Sub-Tab Name' field and save changes
        EXPECTED: * Changes are saved
        EXPECTED: * URL is changed automatically and accordingly to 'SabTab Name' field
        EXPECTED: * URL starts with '/' symbol (e.g '/group1' )
        EXPECTED: * Space in 'Competition Name' field is substituted by '-' symbol in 'URL' field
        EXPECTED: * URL is updated accordingly on Oxygen page
        """
        pass

    def test_009_uncheck_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Uncheck 'Active' checkbox and save changes
        EXPECTED: * Change is saved successfully
        EXPECTED: * SubTab is disabled
        """
        pass

    def test_010_load_oxygen___check_subtab_presence_on_fe(self):
        """
        DESCRIPTION: Load Oxygen -> check SubTab presence on FE
        EXPECTED: Disabled on step #9 SubTab is NOT displayed on FE
        """
        pass

    def test_011_make_some_changes_on_subtab_details_page_click_on_revert_changes_button_and_click_yes_option_on_revert_changes_pop_up(self):
        """
        DESCRIPTION: Make some changes on SubTab Details page, click on 'Revert Changes' button and click 'Yes' option on 'Revert Changes' pop-up
        EXPECTED: * Changes are reverted
        EXPECTED: * 'Save Changes' and 'Revert Changes' buttons are disabled
        """
        pass

    def test_012_make_some_changes_on_subtab_details_page_navigate_to_another_page_via_breadcrumbs_and_click_yes_on_leaving_pop_up(self):
        """
        DESCRIPTION: Make some changes on SubTab Details page, navigate to another page via breadcrumbs and click 'Yes' on 'Leaving' pop-up
        EXPECTED: * Changes on SubTab Details page are NOT saved
        EXPECTED: * User is navigated to corresponding page
        EXPECTED: * 'Save Changes' and 'Revert Changes' buttons are disabled
        """
        pass

    def test_013_go_back_to_subtab_details_page_click_remove_button_and_yes_button_on_remove_pop_up(self):
        """
        DESCRIPTION: Go back to SubTab Details page, click 'Remove' button and 'Yes' button on 'Remove' pop-up
        EXPECTED: * SubTab is no more displayed within the list of all SubTabs
        EXPECTED: * User is navigated to Competition Tab page
        """
        pass

    def test_014_repeat_step_7(self):
        """
        DESCRIPTION: Repeat step #7
        EXPECTED: 
        """
        pass
