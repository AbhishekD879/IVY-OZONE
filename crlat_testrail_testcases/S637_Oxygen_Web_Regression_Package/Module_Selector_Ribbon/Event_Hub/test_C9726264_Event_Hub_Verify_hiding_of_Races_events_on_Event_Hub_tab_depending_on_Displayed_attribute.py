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
class Test_C9726264_Event_Hub_Verify_hiding_of_Races_events_on_Event_Hub_tab_depending_on_Displayed_attribute(Common):
    """
    TR_ID: C9726264
    NAME: Event Hub: Verify hiding of <Races> events on Event Hub tab depending on 'Displayed' attribute
    DESCRIPTION: This test case verifies  hiding of <Races> events on Event Hub tab depending on 'Displayed' attribute
    PRECONDITIONS: 1. To display/undisplay events use http://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. To verify 'Displayed' attribute value check LIVE SERV pushes: Network -> push -> Preview/response tab
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_navigate_to_event_hub_tab(self):
        """
        DESCRIPTION: Load Oxygen application and navigate to Event Hub tab
        EXPECTED: 
        """
        pass

    def test_002_select_any_race_event_from_event_hub_tab(self):
        """
        DESCRIPTION: Select any Race event from Event Hub tab
        EXPECTED: 
        """
        pass

    def test_003_in_ti_tool_undisplay_selected_event_and_save_changesgo_to_oxygen_application_and_verify_event_displaying_on_the_event_hub_tab(self):
        """
        DESCRIPTION: In TI tool undisplay selected event and save changes.
        DESCRIPTION: Go to Oxygen application and verify event displaying on the Event Hub tab
        EXPECTED: Race event is still displayed in application
        """
        pass

    def test_004_refresh_the_page_and_verify_event_displaying_on_the_event_hub_tab(self):
        """
        DESCRIPTION: Refresh the page and verify event displaying on the Event Hub tab
        EXPECTED: Race event is NOT displayed in application
        """
        pass

    def test_005_set_previously_selected_event_to_displayed_and_save_changesgo_to_oxygen_application_and_verify_event_displaying_on_the_event_hub_tab(self):
        """
        DESCRIPTION: Set previously selected event to 'Displayed' and save changes.
        DESCRIPTION: Go to Oxygen application and verify event displaying on the Event Hub tab
        EXPECTED: Event is not displayed on Event Hub tab
        """
        pass

    def test_006_refresh_the_page_and_verify_event_displaying_on_the_event_hub_tab(self):
        """
        DESCRIPTION: Refresh the page and verify event displaying on the Event Hub tab
        EXPECTED: Event is displayed on Event Hub tab
        """
        pass
