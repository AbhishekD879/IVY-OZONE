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
class Test_C1471098_Configure_Specials_Overview_and_Specials_modules(Common):
    """
    TR_ID: C1471098
    NAME: Configure 'Specials-Overview' and 'Specials' modules
    DESCRIPTION: This test case verifies configuration of ''Specials -Overview' and Specials' modules
    PRECONDITIONS: Note: Only valid types and events IDs can be saved for 'Specials -Overview' and Specials' modules
    PRECONDITIONS: * Valid type: (existed type in Backoffice TI)
    PRECONDITIONS: In Backoffice TI Should be checked 'Specials'/'Specials event' flag on all level type->event->market.
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

    def test_002_go_to_big_competition_section___choose_competition___choose_featured_tab(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose 'Featured' tab
        EXPECTED: 'Featured' page is opened
        """
        pass

    def test_003_create_new_module_with_specials_overview_module_type(self):
        """
        DESCRIPTION: Create new Module with 'Specials-Overview' module type
        EXPECTED: Module with 'Specials-Overview' module type is created
        """
        pass

    def test_004_go_to_specials_overview_module_details_page(self):
        """
        DESCRIPTION: Go to 'Specials-Overview' module details page
        EXPECTED: 'Specials-Overview' module details page is loaded
        """
        pass

    def test_005_verify_default_controls_on_module_details_page(self):
        """
        DESCRIPTION: Verify default controls on Module details page
        EXPECTED: * 'Active' check box is unchecked
        EXPECTED: * 'Module Name' (mandatory) field is filled out by set name of the module
        EXPECTED: * 'Module Type' (disabled) field is filled out by selected type value
        EXPECTED: * Event ID or Type Id selector. Default value in Null. It is possible to configure one or multiple types or events by entering Ids come separate.
        EXPECTED: * URL field
        """
        pass

    def test_006_set_events_ids_types_ids_url_tap_reload___apply(self):
        """
        DESCRIPTION: Set:
        DESCRIPTION: * Event's Ids
        DESCRIPTION: * Type's Ids
        DESCRIPTION: * URL
        DESCRIPTION: > Tap 'Reload' -> 'Apply'
        EXPECTED: * In case of entering event Id the event's name is shown
        EXPECTED: * In case of entering type Id the list of valid events  is shown
        """
        pass

    def test_007_tap_save_changes_button(self):
        """
        DESCRIPTION: Tap 'Save Changes' button
        EXPECTED: Success pop-up is displayed
        """
        pass

    def test_008_set_not_valid_types_or_events_type_or_event_are_not_exist_in_back_office_ti(self):
        """
        DESCRIPTION: Set not valid types or events (type or event are not exist in Back office TI)
        EXPECTED: Validation message is shown in case of not existing Id's in Back office TI
        """
        pass

    def test_009_enter_type_or_event_and_that_are_already_saved(self):
        """
        DESCRIPTION: Enter type or event and that are already saved
        EXPECTED: Validation message is shown if event is present on the list of saved events
        """
        pass

    def test_010_enter_type_that_includes_event_from_the_saved_events_list_click_on_the_reload_button(self):
        """
        DESCRIPTION: Enter type that includes event from the saved event's list. Click on the 'Reload' button
        EXPECTED: Existed events are highlighted and type is not applied
        """
        pass

    def test_011_enter_event_that_is_already_saved_from_type_click_on_the_reload_button(self):
        """
        DESCRIPTION: Enter event that is already saved from type. Click on the 'Reload' button
        EXPECTED: Existed events are highlighted and type is not applied
        """
        pass

    def test_012_go_to_big_competition_section___choose_competition___choose_specials_tab(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose 'Specials tab
        EXPECTED: 'Specials' page is opened
        """
        pass

    def test_013_create_new_module_with_specials_specials_type(self):
        """
        DESCRIPTION: Create new Module with 'Specials-Specials' type
        EXPECTED: 'Specials-Specials' module is created
        """
        pass

    def test_014_repeat_steps_from_5_7(self):
        """
        DESCRIPTION: Repeat steps from 5-7
        EXPECTED: * Success pop-up is displayed. Validation message is shown in case of not existing Id's or 'Specials' flag is not check on the market level in Back office TI.
        """
        pass
