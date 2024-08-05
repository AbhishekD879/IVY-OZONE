import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C9726265_Event_Hub_Verify_Featured_Module_displaying_depending_on_events_displaying_parameters_in_the_Module(Common):
    """
    TR_ID: C9726265
    NAME: Event Hub: Verify Featured Module displaying depending on events displaying parameters in the Module
    DESCRIPTION: This test case verifies Featured Module displaying in Event Hub tab depending on events displaying parameters in the Module
    PRECONDITIONS: 1. Event Hub created in CMS > Sport Pages > Event Hub. Featured events  Module with one sport event is created and displayed in application.
    PRECONDITIONS: 2. To display/undisplay event use http://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 3. To verify 'Displayed' attribute value webs socket: Network -> WS -> EIO=3&transport=websocket -> Messages
    PRECONDITIONS: 4. User is on Homepage > Event Hub tab
    """
    keep_browser_open = True

    def test_001_in_ti_tool_undisplay_selected_event_and_save_changesgo_to_oxygen_application_and_verify_the_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: In TI tool undisplay selected event and save changes.
        DESCRIPTION: Go to Oxygen application and verify the event displaying and information received in Live Serve push
        EXPECTED: - displayed:"N" attribute is received in web socket
        EXPECTED: - event stops to display on Featured tab in real time
        EXPECTED: - Featured Events Module stops to display on Event Hub tab in real time
        """
        pass

    def test_002_in_ti_tool_set_previously_selected_event_to_displayed_and_save_changesgo_to_oxygen_application_and_verify_the_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: In TI tool set previously selected event to Displayed and save changes.
        DESCRIPTION: Go to Oxygen application and verify the event displaying and information received in Live Serve push
        EXPECTED: - displayed:"Y" attribute is received in web socket
        EXPECTED: - event starts to display in real time
        EXPECTED: - Featured Events Module starts to display in real time
        """
        pass

    def test_003_make_the_event_live_in_ti_tool_and_save_changes_is_off__yes_and_bet_in_play_list_is_selected(self):
        """
        DESCRIPTION: Make the event LIVE in TI tool and save changes (is OFF = YEs and Bet In Play List is selected)
        EXPECTED: 
        """
        pass

    def test_004_in_ti_tool_set_results_for_selected_event_for_all_selections_and_all_markets_and_save_changesgo_to_oxygen_application_and_verify_the_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: In TI tool set results for selected event (for all selections and all markets) and save changes.
        DESCRIPTION: Go to Oxygen application and verify the event displaying and information received in Live Serve push
        EXPECTED: - an update is received in web socket
        EXPECTED: - event stops to display on Event Hub tab in real time
        EXPECTED: - Featured Events Module stops to display on Events Hub tab in real time
        """
        pass
