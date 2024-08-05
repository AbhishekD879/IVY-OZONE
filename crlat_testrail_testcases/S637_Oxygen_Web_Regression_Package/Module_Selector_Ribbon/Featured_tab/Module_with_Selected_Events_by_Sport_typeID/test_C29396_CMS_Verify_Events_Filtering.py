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
class Test_C29396_CMS_Verify_Events_Filtering(Common):
    """
    TR_ID: C29396
    NAME: CMS: Verify Events Filtering
    DESCRIPTION: This test case verifies Events Filtering/Retrieving.
    PRECONDITIONS: CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_go_to_cms___featured_modules(self):
        """
        DESCRIPTION: Go to CMS -> Featured-modules
        EXPECTED: 
        """
        pass

    def test_002_tap_create_featured_module_button(self):
        """
        DESCRIPTION: Tap 'Create Featured Module' button
        EXPECTED: 
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Fill in all required fields with valid data
        EXPECTED: 
        """
        pass

    def test_004_set_positive_value_into_max_events_to_display_field(self):
        """
        DESCRIPTION: Set positive value into '**Max Events to Display**' field
        EXPECTED: 
        """
        pass

    def test_005_tap_load_selection_button(self):
        """
        DESCRIPTION: Tap '**Load selection**' button
        EXPECTED: All retrieved events are displayed before the '**Loaded from OpenBet' **list
        """
        pass

    def test_006_tap_confirm_selection_button(self):
        """
        DESCRIPTION: Tap '**Confirm Selection**' button
        EXPECTED: List of events from previous step appears below the** 'Events in Module'** list
        """
        pass

    def test_007_verify_clear_events_button(self):
        """
        DESCRIPTION: Verify 'Clear Events' button
        EXPECTED: It is possible to clear confirmed events using 'Clear Events' button
        """
        pass

    def test_008_verify_events_retrieving(self):
        """
        DESCRIPTION: Verify Events Retrieving
        EXPECTED: **- Events are ordered in ascending by event startTime before retrieving**
        EXPECTED: **- Suspended events (eventStatusCode="S") are filter out**
        EXPECTED: **- Each Not Outright event has Primary Market (market with dispSortName="HH" or "MR")**
        EXPECTED: **- Outrights have ​'**eventSortCode="TNMT"/"MTCH"/"TR01-TR20"'****
        EXPECTED: - Events without markets are filtered out
        EXPECTED: - Events with NO outcomes within Primary/selected market are filtered out
        """
        pass

    def test_009_verify_number_of_retrieved_events(self):
        """
        DESCRIPTION: Verify number of retrieved events
        EXPECTED: Number of retrieved events corresponds to value set on step №4
        """
        pass

    def test_010_tap_save_module_button(self):
        """
        DESCRIPTION: Tap 'Save Module' button
        EXPECTED: 
        """
        pass

    def test_011_load_invictus_application_and_verify_created_module(self):
        """
        DESCRIPTION: Load Invictus application and verify created module
        EXPECTED: Module is displayed on the Featured tab
        """
        pass

    def test_012_verify_list_of_events_in_this_module(self):
        """
        DESCRIPTION: Verify list of events in this module
        EXPECTED: List/number of events corresponds to steps №8-9
        """
        pass
