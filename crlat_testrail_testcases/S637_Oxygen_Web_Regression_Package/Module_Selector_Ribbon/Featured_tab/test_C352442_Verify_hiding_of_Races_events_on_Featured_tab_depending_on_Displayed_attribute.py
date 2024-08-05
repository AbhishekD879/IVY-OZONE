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
class Test_C352442_Verify_hiding_of_Races_events_on_Featured_tab_depending_on_Displayed_attribute(Common):
    """
    TR_ID: C352442
    NAME: Verify hiding of <Races> events on Featured tab depending on 'Displayed' attribute
    DESCRIPTION: This test case verifies  hiding of <Races> events on Featured tab depending on 'Displayed' attribute
    PRECONDITIONS: 1. To display/undisplay events use ttp://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. To verify 'Displayed' attribute value check Featured webSocket: Network -> WS -> wss://featured-sports.coralsports.nonprod.cloud.ladbrokescoral.com/socket.io/?EIO=3&transport=websocket
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_navigate_to_featured_tab(self):
        """
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        EXPECTED: 
        """
        pass

    def test_002_select_any_race_event_from_featured_tab(self):
        """
        DESCRIPTION: Select any Race event from Featured tab
        EXPECTED: 
        """
        pass

    def test_003_in_ti_tool_undisplay_selected_event_and_save_changesgo_to_oxygen_application_and_verify_event_displaying_on_the_featured_tab(self):
        """
        DESCRIPTION: In TI tool undisplay selected event and save changes.
        DESCRIPTION: Go to Oxygen application and verify event displaying on the Featured tab
        EXPECTED: - displayed:"N" attribute is received in Featured webSocket
        EXPECTED: - event stops to display on Featured tab in real time
        """
        pass

    def test_004_refresh_the_page_and_verify_event_displaying_on_the_featured_tab(self):
        """
        DESCRIPTION: Refresh the page and verify event displaying on the Featured tab
        EXPECTED: Race event is NOT displayed in application
        """
        pass

    def test_005_set_previously_selected_event_to_displayed_and_save_changesgo_to_oxygen_application_and_verify_event_displaying_on_the_featured_tab(self):
        """
        DESCRIPTION: Set previously selected event to 'Displayed' and save changes.
        DESCRIPTION: Go to Oxygen application and verify event displaying on the Featured tab
        EXPECTED: - displayed:"Y" attribute is received in Featured webSocket
        EXPECTED: - event doesn't appear on Featured tab in real time
        """
        pass

    def test_006_refresh_the_page_and_verify_event_displaying_on_the_featured_tab(self):
        """
        DESCRIPTION: Refresh the page and verify event displaying on the Featured tab
        EXPECTED: Event is displayed on Featured tab
        """
        pass
