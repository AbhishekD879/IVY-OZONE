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
class Test_C352441_Hiding_Events_on_Featured_tab_depending_on_result_conf_attribute(Common):
    """
    TR_ID: C352441
    NAME: Hiding Events on Featured tab depending on 'result_conf' attribute
    DESCRIPTION: This test case verifies Hiding Events on Featured tab depending on 'result_conf' attribute
    DESCRIPTION: NEEDS TO BE UPDATED: 'result_conf' attribute is received in WS, not in push
    PRECONDITIONS: 1. To set result for event use http://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. To verify 'result_conf' attribute value check LIVE SERV pushes: Network -> push -> Preview/response tab
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_navigate_to_featured_tab(self):
        """
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        EXPECTED: 
        """
        pass

    def test_002_select_any_live_sport_event_from_featured_tab(self):
        """
        DESCRIPTION: Select any LIVE sport event from Featured tab
        EXPECTED: 
        """
        pass

    def test_003_in_ti_tool_set_results_for_selected_event_and_save_changesgo_to_oxygen_application_and_verify_the_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: In TI tool set results for selected event and save changes.
        DESCRIPTION: Go to Oxygen application and verify the event displaying and information received in Live Serve push
        EXPECTED: - result_conf:”Y” attribute is received in Live Serve push
        EXPECTED: - event stops to display on Featured tab in real time
        """
        pass

    def test_004_(self):
        """
        DESCRIPTION: 
        EXPECTED: 
        """
        pass
