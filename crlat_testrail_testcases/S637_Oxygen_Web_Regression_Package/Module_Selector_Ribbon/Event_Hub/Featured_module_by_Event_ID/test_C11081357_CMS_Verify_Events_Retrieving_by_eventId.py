import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C11081357_CMS_Verify_Events_Retrieving_by_eventId(Common):
    """
    TR_ID: C11081357
    NAME: CMS: Verify Events Retrieving by eventId
    DESCRIPTION: This test case verifies Events Retrieving by eventId
    PRECONDITIONS: 1. To get SiteServer info about an event, use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - currently supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: NOTE: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 2. Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 3. A user is on the Homepage > Event Hub tab.
    """
    keep_browser_open = True

    def test_001_go_to_cms__sports_pages__eventhub__featured_events_module(self):
        """
        DESCRIPTION: Go to CMS > Sports Pages > EventHub > "Featured events" module
        EXPECTED: 
        """
        pass

    def test_002_tap_create_featured_tab_module_button(self):
        """
        DESCRIPTION: Tap 'Create Featured Tab Module' button
        EXPECTED: 
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data_go_to_select_events_by_field_and_select_eventnote_date_range_is_not_taken_into_account_when_retrieving_events_by_eventid_marketid_and_selectionid(self):
        """
        DESCRIPTION: Fill in all required fields with valid data, go to 'Select Events by' field and select "Event"
        DESCRIPTION: NOTE: Date range is not taken into account when retrieving events by eventId, marketId and selectionId.
        EXPECTED: * "Note: Racing events are not supported." warning message is shown
        """
        pass

    def test_004_in_backoffice_find_any_undisplayed_event(self):
        """
        DESCRIPTION: In Backoffice, find any Undisplayed Event
        EXPECTED: 
        """
        pass

    def test_005_go_back_to_cms_and_enter_eventid_of_the_eventnot_racing_from_step_4_into_id_fieldpress_reload_button_and_verify_the_retrieving_of_the_selected_event(self):
        """
        DESCRIPTION: Go back to CMS and enter eventId of the event(not Racing) from Step 4 into 'Id' field
        DESCRIPTION: Press 'Reload' button and verify the retrieving of the selected Event.
        EXPECTED: * Undisplayed Event is not loaded to CMS
        """
        pass

    def test_006_enter_any_active_eventid_to_id_fieldpress_reload_button_and_verify_the_retrieving_of_the_selected_event(self):
        """
        DESCRIPTION: Enter any active eventId to "Id" field.
        DESCRIPTION: Press 'Reload' button and verify the retrieving of the selected Event.
        EXPECTED: * Event is successfully loaded to CMS
        """
        pass

    def test_007_tap_save_module_button(self):
        """
        DESCRIPTION: Tap 'Save Module' button
        EXPECTED: * Module is saved
        """
        pass
