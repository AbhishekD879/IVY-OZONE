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
class Test_C355731_Verify_Featured_Module_displaying_depending_on_events_displaying_parameters_in_the_Module(Common):
    """
    TR_ID: C355731
    NAME: Verify Featured Module displaying depending on events displaying parameters in the Module
    DESCRIPTION: This test case verifies Featured Module displaying depending on events displaying parameters in the Module
    PRECONDITIONS: 1. Featured Tab Module with one sport event is created and displayed in applciation.
    PRECONDITIONS: 2. To display/undisplay event use http://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. To verify 'Displayed' attribute value check LIVE SERV pushes: Network -> push -> Preview/response tab
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_navigate_to_featured_tab(self):
        """
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        EXPECTED: 
        """
        pass

    def test_002_select_featured_tab_module_with_one_sport_event(self):
        """
        DESCRIPTION: Select Featured Tab Module with one sport event
        EXPECTED: 
        """
        pass

    def test_003_in_ti_tool_undisplay_selected_event_and_save_changesgo_to_oxygen_application_and_verify_the_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: In TI tool undisplay selected event and save changes.
        DESCRIPTION: Go to Oxygen application and verify the event displaying and information received in Live Serve push
        EXPECTED: - displayed:"N" attribute is received in Live Serve push
        EXPECTED: - event stops to display on Featured tab in real time
        EXPECTED: - Featured Tab Module stops to display on Featured tab in real time
        """
        pass

    def test_004_in_ti_tool_set_previously_selected_event_to_displayed_and_save_changesgo_to_oxygen_application_and_verify_the_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: In TI tool set previously selected event to Displayed and save changes.
        DESCRIPTION: Go to Oxygen application and verify the event displaying and information received in Live Serve push
        EXPECTED: - displayed:"Y" attribute is received in Live Serve push
        EXPECTED: - event starts to display in real time
        EXPECTED: - Featured Tab Module starts to display in real time
        """
        pass

    def test_005_make_the_event_live_in_ti_tool_and_save_changes_is_off__yes_and_bet_in_play_list_is_selected(self):
        """
        DESCRIPTION: Make the event LIVE in TI tool and save changes (is OFF = YEs and Bet In Play List is selected)
        EXPECTED: 
        """
        pass

    def test_006_in_ti_tool_set_results_for_selected_event_for_all_selections_and_all_markets_and_save_changesgo_to_oxygen_application_and_verify_the_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: In TI tool set results for selected event (for all selections and all markets) and save changes.
        DESCRIPTION: Go to Oxygen application and verify the event displaying and information received in Live Serve push
        EXPECTED: - result_conf:”Y” attribute is received in Live Serve push
        EXPECTED: - event stops to display on Featured tab in real time
        EXPECTED: - Featured Tab Module stops to display on Featured tab in real time
        """
        pass
