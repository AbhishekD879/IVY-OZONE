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
class Test_C9726262_Event_hub_Hiding_Events_on_Event_Hub_tab_depending_on_Displayed_attribute(Common):
    """
    TR_ID: C9726262
    NAME: Event hub: Hiding Events on Event Hub tab depending on 'Displayed' attribute
    DESCRIPTION: This test case verifies Hiding Events on Event hub tab depending on Displayed attribute
    PRECONDITIONS: 1. To display/undisplay event use http://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. To verify 'Displayed' attribute value check Featured webSocket: Network -> WS -> wss://featured-sports.coralsports.nonprod.cloud.ladbrokescoral.com/socket.io/?EIO=3&transport=websocket
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_navigate_to_event_hub_tab(self):
        """
        DESCRIPTION: Load Oxygen application and navigate to Event Hub tab
        EXPECTED: 
        """
        pass

    def test_002_select_any_sport_event__from_event_hub_tab(self):
        """
        DESCRIPTION: Select any sport event  from Event Hub tab
        EXPECTED: 
        """
        pass

    def test_003_in_ti_tool_undisplay_selected_event_and_save_changesgo_to_oxygen_application_and_verify_the_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: In TI tool undisplay selected event and save changes.
        DESCRIPTION: Go to Oxygen application and verify the event displaying and information received in Live Serve push
        EXPECTED: - displayed:"N" attribute is received in Featured WebSocket
        EXPECTED: - event stops to display on Event Hub tab in real time
        """
        pass

    def test_004_in_ti_tool_set_previously_selected_event_to_displayed_and_save_changesgo_to_oxygen_application_and_verify_the_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: In TI tool set previously selected event to Displayed and save changes.
        DESCRIPTION: Go to Oxygen application and verify the event displaying and information received in Live Serve push
        EXPECTED: - displayed:"Y" attribute is received in Featured WebSocket
        EXPECTED: - event does NOT start to display in real time
        """
        pass

    def test_005_refresh_the_page_and_verify_the_event_displaying(self):
        """
        DESCRIPTION: Refresh the page and verify the event displaying
        EXPECTED: Event starts to display on Event Hub tab
        """
        pass
