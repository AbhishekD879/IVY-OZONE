import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C58446955_Featured_Module__Verify_Virtual_Horse_racing_Greyhounds_Events_Retrieving_by_Race_TypeID(Common):
    """
    TR_ID: C58446955
    NAME: Featured Module -  Verify Virtual Horse racing/Greyhounds Events Retrieving by <Race> TypeID
    DESCRIPTION: This test case verifies events retrieving by <Race> TypeID for Virtual Horse racing/Greyhounds events.
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) To check <Race> TypeID go to(for beta):
    PRECONDITIONS: Virtual Horse Racing - https://obbackoffice-ladbrokes.dub1.egalacoral.com/ti/hierarchy/class/285 (check TypeID's below this class)
    PRECONDITIONS: Virtual Greyhounds - https://obbackoffice-ladbrokes.dub1.egalacoral.com/ti/hierarchy/class/286 (check TypeID's below this class)
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_reach_featured_tab_modules(self):
        """
        DESCRIPTION: Go to CMS and reach Featured Tab Modules
        EXPECTED: 
        """
        pass

    def test_002_tap_on_create_featured_tab_module_button(self):
        """
        DESCRIPTION: Tap on 'Create Featured Tab Module' button
        EXPECTED: Feature Tab Module form is opened.
        EXPECTED: (Fill in all required fields with valid data)
        """
        pass

    def test_003_go_to_select_events_by_field_and_select_race_type_id(self):
        """
        DESCRIPTION: Go to 'Select Events by' field and select Race Type ID
        EXPECTED: 
        """
        pass

    def test_004_set_valid_race_type_id(self):
        """
        DESCRIPTION: Set valid <Race> Type ID
        EXPECTED: Entered <Race> Type ID is shown
        """
        pass

    def test_005_tap_reload_button_in_loaded_from_openbet_column(self):
        """
        DESCRIPTION: Tap 'Reload' button in "Loaded from OpenBet" column
        EXPECTED: Events should appear in left column "Events in Module"
        """
        pass

    def test_006_tap_apply_button(self):
        """
        DESCRIPTION: Tap 'Apply' button
        EXPECTED: Events should move to the right column.
        EXPECTED: (Tap 'Save changes' button to save your Module).
        """
        pass

    def test_007_load_application_and_verify_events_within_created_module_in_homepage(self):
        """
        DESCRIPTION: Load application and verify events within created Module in Homepage
        EXPECTED: All Virtuals events are shown in Featured Module and have the same <Race> TypeId as was set on step 5.
        """
        pass

    def test_008_create_module_with_greyhounds_race_typeid_using_the_same_flow_as_above(self):
        """
        DESCRIPTION: Create module with Greyhounds <Race> TypeID using the same flow as above.
        EXPECTED: GH Virtuals events are shown in Featured Module.
        """
        pass
