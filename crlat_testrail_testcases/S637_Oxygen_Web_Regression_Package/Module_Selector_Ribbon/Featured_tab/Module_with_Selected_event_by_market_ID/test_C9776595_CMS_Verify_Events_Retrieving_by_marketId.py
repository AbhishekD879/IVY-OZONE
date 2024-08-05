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
class Test_C9776595_CMS_Verify_Events_Retrieving_by_marketId(Common):
    """
    TR_ID: C9776595
    NAME: CMS: Verify Events Retrieving by marketId
    DESCRIPTION: This test case verifies Events Retrieving by marketId
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_go_to_cms___featured_tab_modules(self):
        """
        DESCRIPTION: Go to CMS -> Featured Tab Modules
        EXPECTED: 
        """
        pass

    def test_002_tap_create_featured_tab_module_button(self):
        """
        DESCRIPTION: Tap 'Create Featured Tab Module' button
        EXPECTED: 
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data_go_to_select_eventsby_field_and_select__marketnote_date_range_is_not_taken_into_account_when_retrieving_events_by_eventid_marketid_and_selectionid(self):
        """
        DESCRIPTION: Fill in all required fields with valid data, go to 'Select Events by' field and select  "Market"
        DESCRIPTION: NOTE: Date range is not taken into account when retrieving events by eventId, marketId and selectionId.
        EXPECTED: * "Note: Only primary markets, outright markets, Win or Each Way markets supported." warning message is shown.
        """
        pass

    def test_004_in_backoffice_find_any_undisplayed_event___select_any_market_from_this_event(self):
        """
        DESCRIPTION: In Backoffice, find any Undisplayed Event -> select any market from this event
        EXPECTED: 
        """
        pass

    def test_005_go_back_to_cms_and_enter_marketid_of_the_market_from_step_4_into_id_fieldpress_reload_button_and_verify_the_retrieving_of_selected_event(self):
        """
        DESCRIPTION: Go back to CMS and enter marketId of the market from Step 4 into 'Id' field
        DESCRIPTION: Press 'Reload' button and verify the retrieving of selected Event.
        EXPECTED: * Undisplayed Event is not loaded to CMS
        """
        pass

    def test_006_in_backoffice_display_back_event_from_step_4___select_a_market_of_this_event_and_undisplay_it(self):
        """
        DESCRIPTION: In Backoffice, display back Event from Step 4 -> select a market of this event and undisplay it.
        EXPECTED: 
        """
        pass

    def test_007_go_back_to_cms_and_enter_marketid_of_the_market_from_step_6_into_id_fieldpress_reload_button_and_verify_the_retrieving_of_selected_event(self):
        """
        DESCRIPTION: Go back to CMS and enter marketId of the market from Step 6 into 'Id' field
        DESCRIPTION: Press 'Reload' button and verify the retrieving of selected Event.
        EXPECTED: * Event with undisplayed market is not loaded
        """
        pass

    def test_008_enter_any_marketid_of_the_active_market_from_any_active_eventpress_reload_button_and_verify_the_retrieving_of_selected_event(self):
        """
        DESCRIPTION: Enter any marketId of the active market from any active Event.
        DESCRIPTION: Press 'Reload' button and verify the retrieving of selected Event.
        EXPECTED: * Event is successfully loaded to CMS
        """
        pass

    def test_009_tap_save_module_button(self):
        """
        DESCRIPTION: Tap 'Save Module' button
        EXPECTED: Module is saved
        """
        pass
