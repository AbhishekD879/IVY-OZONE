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
class Test_C1316454_Configure_Module_Outright(Common):
    """
    TR_ID: C1316454
    NAME: Configure Module Outright
    DESCRIPTION: This test verifies configuration of Module Outright.
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

    def test_002_go_to_big_competition_section___choose_competition___choose_tab_that_has_inactive_subtabs_option__choose_a_sub_tab(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has inactive SubTabs option > choose a Sub-tab
        EXPECTED: Tab landing page is opened
        """
        pass

    def test_003_create_new_module_with_outright_type(self):
        """
        DESCRIPTION: Create new Module with 'Outright' type
        EXPECTED: * New module with 'Outright' type is created
        EXPECTED: * New module is disabled by default
        """
        pass

    def test_004_go_to_module_details_page(self):
        """
        DESCRIPTION: Go to Module details page
        EXPECTED: 'Outright' Module details page is loaded
        """
        pass

    def test_005_select_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Select 'Active' checkbox and save changes
        EXPECTED: Module is enabled
        """
        pass

    def test_006_click_add_ob_market_id_button(self):
        """
        DESCRIPTION: Click 'Add OB Market ID' button
        EXPECTED: * 'Add OB Market ID' pop-up is displayed
        """
        pass

    def test_007_verify_active_checkbox(self):
        """
        DESCRIPTION: Verify 'Active' checkbox
        EXPECTED: * 'Active' checkbox is unchecked by default
        EXPECTED: * 'Active' checkbox determines whether Market will be shown on FE within Module
        EXPECTED: * 'Active' checkbox is NOT mandatory
        """
        pass

    def test_008_verify_collapsed_checkbox(self):
        """
        DESCRIPTION: Verify 'Collapsed' checkbox
        EXPECTED: * 'Collapsed' checkbox is unchecked by default
        EXPECTED: * 'Collapsed' checkbox determines whether Market panel will be shown in collapsed/expanded state
        EXPECTED: on FE within Module
        EXPECTED: * 'Collapsed' checkbox is NOT mandatory
        """
        pass

    def test_009_verify_ob_market_id_field(self):
        """
        DESCRIPTION: Verify 'OB Market ID' field
        EXPECTED: 'OB Market ID' field is mandatory
        """
        pass

    def test_010_verify_override_market_name_field(self):
        """
        DESCRIPTION: Verify 'Override Market Name' field
        EXPECTED: * 'Override Market Name' field is not mandatory
        EXPECTED: * 'Override Market Name' field is disabled by default
        """
        pass

    def test_011_verify_max_displayed_field(self):
        """
        DESCRIPTION: Verify 'Max Displayed' field
        EXPECTED: * 'Max display' value determines the number of outcomes within market that will be visible on FE
        EXPECTED: * The rest of outcome will be reviewed by using 'Show More' option
        EXPECTED: * 'Max Displayed' field is mandatory
        """
        pass

    def test_012_verify_listgridcard_radio_button(self):
        """
        DESCRIPTION: Verify 'List/Grid/Card' radio button
        EXPECTED: * 'List/Grid/Card' radio button is mandatory to select
        EXPECTED: * 'List/Grid/Card is unselected by default
        EXPECTED: * 'List/Grid/Card' option determines the view that will be shown for events within Module on FE
        """
        pass

    def test_013_enter_incorrect_market_id_in_ob_market_id_field_and_click_upload_market_name_button(self):
        """
        DESCRIPTION: Enter incorrect Market ID in 'OB Market ID' field and click 'Upload Market Name' button
        EXPECTED: * Error message is displayed next 'OB Market ID' field
        EXPECTED: * Market data is NOT loaded into Module
        """
        pass

    def test_014_enter_correct_market_id_in_ob_market_id_field_and_click_upload_market_name_button(self):
        """
        DESCRIPTION: Enter correct Market ID in 'OB Market ID' field and click 'Upload Market Name' button
        EXPECTED: * Market data is loaded into Module
        EXPECTED: * 'Override Market Name' field becomes enabled and populated by Market Name value
        EXPECTED: * Market Name value corresponds to OB **marketName** attribute
        """
        pass

    def test_015_set_listgridcard_option_numerical_value_in_max_displayed_fieldand_click_save_changes_button(self):
        """
        DESCRIPTION: Set
        DESCRIPTION: * 'List/Grid/Card' option
        DESCRIPTION: * numerical value in 'Max Displayed' field
        DESCRIPTION: and click 'Save Changes' button
        EXPECTED: * New Market is added to the list of all Outright Module
        EXPECTED: * 'List/Grid/Card' option is selected
        EXPECTED: * 'Max Displayed' is set up
        """
        pass

    def test_016_click_on_pen_to_edit_added_on_step_14_market(self):
        """
        DESCRIPTION: Click on pen to edit added on step #14 Market
        EXPECTED: * 'Edit OB Market ID' is displayed
        EXPECTED: * Data set up on step #14 is displayed and stored
        """
        pass

    def test_017_set_and_edit_active_checkbox_show_expanded_checkbox_override_market_name_fieldand_click_save_changes_button(self):
        """
        DESCRIPTION: Set and edit
        DESCRIPTION: * 'Active' checkbox
        DESCRIPTION: * 'Show Expanded' checkbox
        DESCRIPTION: * 'Override Market Name' field
        DESCRIPTION: and click 'Save Changes' button
        EXPECTED: * Changes are saved and listed within Market Table
        EXPECTED: * Market becomes enabled and collapsed on FE
        EXPECTED: * Market name changes according to new value
        """
        pass

    def test_018_add_a_few_markets_to_module(self):
        """
        DESCRIPTION: Add a few Markets to Module
        EXPECTED: Markets are added and listed within Module
        """
        pass

    def test_019_change_order_of_markets_by_drag_n_drop(self):
        """
        DESCRIPTION: Change order of Markets by drag-n-drop
        EXPECTED: Order is changed
        """
        pass

    def test_020_tap_on_the_bin_sign_button_opposite_to_particular_market_in_table(self):
        """
        DESCRIPTION: Tap on the bin sign button opposite to particular Market in Table
        EXPECTED: * Respective Market is removed from Module
        EXPECTED: * User stays in Module landing page
        """
        pass

    def test_021_go_to_big_competition_section___choose_competition___choose_tab_that_does_not_have_active_subtabs_option(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that does NOT have active SubTabs option
        EXPECTED: Tab landing page is opened
        """
        pass

    def test_022_repeat_step_4_20(self):
        """
        DESCRIPTION: Repeat step #4-20
        EXPECTED: 
        """
        pass
