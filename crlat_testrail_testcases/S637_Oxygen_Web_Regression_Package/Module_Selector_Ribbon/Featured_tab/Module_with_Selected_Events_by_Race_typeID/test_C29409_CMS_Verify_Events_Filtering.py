import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C29409_CMS_Verify_Events_Filtering(Common):
    """
    TR_ID: C29409
    NAME: CMS: Verify Events Filtering
    DESCRIPTION: This test case verifies Events Filtering/Retrieving.
    DESCRIPTION: **Jira tickets:** BMA-6571 CMS: Featured Tab Module - Horse Racing
    PRECONDITIONS: - CMS https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
    PRECONDITIONS: - Ladbrokes OpenBet System https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    PRECONDITIONS: - Coral OpenBet System https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: "Auto-refresh events" Checkbox is not checked
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_open_featured_tab_modulesclick_create_featured_tab_module_button(self):
        """
        DESCRIPTION: Go to CMS and open FEATURED TAB MODULES
        DESCRIPTION: Click "Create FEATURED TAB MODULE" button
        EXPECTED: 
        """
        pass

    def test_002_fill_in_all_required_fields_with_valid_data_to_create_module_by_race_typeid(self):
        """
        DESCRIPTION: Fill in all required fields with valid data to create **module by <Race> typeID**
        EXPECTED: 
        """
        pass

    def test_003_set_positive_value_into_max_events_to_display_field(self):
        """
        DESCRIPTION: Set positive value into '**Max Events to Display**' field
        EXPECTED: 
        """
        pass

    def test_004_tap_load_selection_button(self):
        """
        DESCRIPTION: Tap '**Load selection**' button
        EXPECTED: All retrieved events are displayed before the '**Loaded from OpenBet' **list
        """
        pass

    def test_005_tap_confirm_selection_button(self):
        """
        DESCRIPTION: Tap '**Confirm Selection**' button
        EXPECTED: List of events from previous step appears below the** 'Events in Module'** list
        """
        pass

    def test_006_verify_clear_events_button(self):
        """
        DESCRIPTION: Verify '**Clear Events**' button
        EXPECTED: It is possible to clear confirmed events using 'Clear Events' button
        """
        pass

    def test_007_verify_events_retrieving(self):
        """
        DESCRIPTION: Verify Events Retrieving
        EXPECTED: **- Events are ordered in ascending by event displayOrder before retrieving**
        EXPECTED: **- Each event has market 'name="Win or Each Way"' (with collectionNames="Win or Each Way,")**
        EXPECTED: - Events with NO outcomes within "Win or Each Way" market are filtered out
        """
        pass

    def test_008_verify_number_of_retrieved_events(self):
        """
        DESCRIPTION: Verify number of retrieved events
        EXPECTED: Number of retrieved events corresponds to value set in step №4
        """
        pass

    def test_009_tap_save_module_button(self):
        """
        DESCRIPTION: Tap '**Save Module**' button
        EXPECTED: Module is saved
        """
        pass

    def test_010_load_application_and_verify_created_module(self):
        """
        DESCRIPTION: Load application and verify created module
        EXPECTED: Module is displayed within the Featured tab
        """
        pass

    def test_011_verify_list_of_events_in_this_module(self):
        """
        DESCRIPTION: Verify list of events in this module
        EXPECTED: List/number of events corresponds to steps №8-9
        """
        pass
