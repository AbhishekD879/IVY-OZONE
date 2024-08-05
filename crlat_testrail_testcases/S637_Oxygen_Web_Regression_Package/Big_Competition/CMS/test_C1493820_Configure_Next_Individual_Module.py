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
class Test_C1493820_Configure_Next_Individual_Module(Common):
    """
    TR_ID: C1493820
    NAME: Configure 'Next Individual' Module
    DESCRIPTION: 
    PRECONDITIONS: 
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

    def test_003_create_new_module_with_next_individual_type(self):
        """
        DESCRIPTION: Create new Module with 'Next Individual' type
        EXPECTED: * New module with 'Next Individual' type is created
        EXPECTED: * New module is disabled by default
        """
        pass

    def test_004_go_to_module_details_page(self):
        """
        DESCRIPTION: Go to Module details page
        EXPECTED: Module details page is loaded
        """
        pass

    def test_005_verify_all_buttons_are_working_properly(self):
        """
        DESCRIPTION: Verify all buttons are working properly
        EXPECTED: * Active checkbox, which defines active/inactive module
        EXPECTED: * Max Display, mandatory field that only allows positive integer numbers
        EXPECTED: * Default view, with 'List' and 'Card' view available checkboxes
        """
        pass

    def test_006_add_a_valid_event_id_to_add_event_id_field_and_tap_reload(self):
        """
        DESCRIPTION: Add a valid Event Id to 'Add Event Id' field and tap 'Reload'
        EXPECTED: Event name is added below 'Loaded from Openbet'
        """
        pass

    def test_007_tap_apply(self):
        """
        DESCRIPTION: Tap 'Apply'
        EXPECTED: Event name is added below 'Events in Module'
        """
        pass

    def test_008_repeat_step_6_with_the_same_event_id(self):
        """
        DESCRIPTION: Repeat step 6 with the same event Id
        EXPECTED: Event is not added and a red warning message is shown: "Event ID already exists in events list"
        """
        pass

    def test_009_in_backoffice_set_the_event_to_undisplayedcome_back_to_cms_and_refresh(self):
        """
        DESCRIPTION: In Backoffice set the event to 'Undisplayed'
        DESCRIPTION: Come back to CMS and refresh
        EXPECTED: Respective event Id font is changed to red and a red warning message is shown: "Invalid Event ID's. Please remove all"
        EXPECTED: A red button is displayed named 'Remove Invalid Ids'
        """
        pass

    def test_010_tap_on_red_button_named_remove_invalid_ids(self):
        """
        DESCRIPTION: Tap on red button named 'Remove Invalid Ids'
        EXPECTED: Respective Event Ids are removed
        """
        pass

    def test_011_in_backoffice_set_the_event_to_displayed(self):
        """
        DESCRIPTION: In Backoffice set the event to 'Displayed'
        EXPECTED: 
        """
        pass

    def test_012_repeat_step_6___7(self):
        """
        DESCRIPTION: Repeat step 6 - 7
        EXPECTED: Event market name is added below 'Events in Module
        """
        pass

    def test_013_tap_on_revert_changes(self):
        """
        DESCRIPTION: Tap on 'Revert changes'
        EXPECTED: Event market name is removed
        """
        pass

    def test_014_repeat_step_6___7_adding_two_valid_event_ids_and_press_save_changes(self):
        """
        DESCRIPTION: Repeat step 6 - 7, adding two valid event Ids and press 'Save changes'
        EXPECTED: Events market names are added below 'Events in Module'
        """
        pass

    def test_015_delete_on_of_the_events_from_events_in_module(self):
        """
        DESCRIPTION: Delete on of the events from 'Events in Module'
        EXPECTED: Respective event market name is removed from 'Events in Module'
        """
        pass

    def test_016_tap_on_revert_changes(self):
        """
        DESCRIPTION: Tap on 'Revert changes'
        EXPECTED: Previous event market name deleted is added again to 'Events in Module'
        """
        pass

    def test_017_repeat_step_6___7_adding_one_undisplayed_event(self):
        """
        DESCRIPTION: Repeat step 6 - 7, adding one undisplayed event
        EXPECTED: Event Id is NOT added below 'Loaded from Openbet'
        """
        pass
