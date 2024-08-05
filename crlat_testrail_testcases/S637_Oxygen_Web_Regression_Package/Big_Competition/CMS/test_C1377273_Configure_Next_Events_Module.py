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
class Test_C1377273_Configure_Next_Events_Module(Common):
    """
    TR_ID: C1377273
    NAME: Configure 'Next Events' Module
    DESCRIPTION: This test case verifies configuration of 'Next Events' Module
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

    def test_002_go_to_big_competition_section___choose_competition___choose_tab_that_has_subtabs_option__choose_a_sub_tab(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has SubTabs option > choose a Sub-tab
        EXPECTED: Sub-Tab landing page is opened
        """
        pass

    def test_003_create_new_module_with_next_events_type(self):
        """
        DESCRIPTION: Create new Module with 'Next Events' type
        EXPECTED: * New module with 'Next Events' type is created
        EXPECTED: * New module is disabled by default
        """
        pass

    def test_004_go_to_module_details_page(self):
        """
        DESCRIPTION: Go to Module details page
        EXPECTED: Module details page is loaded
        """
        pass

    def test_005_select_active_checkbox(self):
        """
        DESCRIPTION: Select 'Active' checkbox
        EXPECTED: * 'Save Changes' button should be inactive
        EXPECTED: * 'TypeId should be entered' error for OB Type ID field is displayed
        """
        pass

    def test_006_verify_ob_type_id_field(self):
        """
        DESCRIPTION: Verify 'OB Type ID' field
        EXPECTED: * 'OB Type ID' field is mandatory
        """
        pass

    def test_007_verify_max_display_field(self):
        """
        DESCRIPTION: Verify 'Max display' field
        EXPECTED: * 'Max display' value determines the number of events within particular type displayed within Module
        EXPECTED: * 'Max display' field is mandatory
        EXPECTED: * Default value is 10
        """
        pass

    def test_008_verify_listcard_view_radio_button(self):
        """
        DESCRIPTION: Verify 'List/Card View' radio button
        EXPECTED: * 'List/Card' radio button is mandatory to select
        EXPECTED: * 'Card View' is default option
        EXPECTED: * 'List/Card' option determines the view that will be shown for events within Module on FE
        """
        pass

    def test_009_enter_correct_value_in_max_display_field_choose_listcard_optionand_incorrect_type_id_in__ob_type_id_fieldand_click_save_changes_button(self):
        """
        DESCRIPTION: Enter correct
        DESCRIPTION: * value in 'Max display' field
        DESCRIPTION: * choose List/Card option
        DESCRIPTION: and incorrect
        DESCRIPTION: * type ID in  'OB Type ID' field
        DESCRIPTION: and click 'Save Changes' button
        EXPECTED: * Error message is displayed
        EXPECTED: * List of events within type is NOT loaded into Module
        EXPECTED: * User stays on current page
        """
        pass

    def test_010_enter_correct_choose_listcard_option_type_id_in_ob_type_id_field_for_max_display_field_leave_default_valueand_click_save_changes_button(self):
        """
        DESCRIPTION: Enter correct
        DESCRIPTION: * choose List/Card option
        DESCRIPTION: * type ID in 'OB Type ID' field
        DESCRIPTION: * For 'Max display' field leave default value
        DESCRIPTION: and click 'Save Changes' button
        EXPECTED: * Success pop-up is displayed
        EXPECTED: * List of all events within type is loaded into Module
        """
        pass

    def test_011_enter_correct_value_in_max_display_field_not_default_choose_listcard_option_type_id_in_ob_type_id_field(self):
        """
        DESCRIPTION: Enter correct
        DESCRIPTION: * value in 'Max display' field (not default)
        DESCRIPTION: * choose List/Card option
        DESCRIPTION: * type ID in 'OB Type ID' field
        EXPECTED: * Success pop-up is displayed
        EXPECTED: * Number of events set up in 'Max display' field is loaded into Module
        """
        pass

    def test_012_go_to_big_competition_section___choose_competition___choose_tab_that_has_no_subtabs_option_set(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has no SubTabs option set
        EXPECTED: Tab landing page is opened
        """
        pass

    def test_013_repeat_steps_3_11(self):
        """
        DESCRIPTION: Repeat steps #3-11
        EXPECTED: 
        """
        pass
