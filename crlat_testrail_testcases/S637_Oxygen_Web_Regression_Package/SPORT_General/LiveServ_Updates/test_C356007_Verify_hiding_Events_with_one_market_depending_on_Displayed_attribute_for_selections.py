import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C356007_Verify_hiding_Events_with_one_market_depending_on_Displayed_attribute_for_selections(Common):
    """
    TR_ID: C356007
    NAME: Verify hiding Events with one market depending on 'Displayed' attribute for selections
    DESCRIPTION: This test case verifies hiding Events with one market depending on 'Displayed' attribute for selections
    DESCRIPTION: AUTOTEST [C2496187]
    PRECONDITIONS: 1. To display/undisplay event/market/selection use http://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. Create event that has only ONE market
    PRECONDITIONS: 3. To check updates open Dev Tools -> Network tab -> WS option
    PRECONDITIONS: Endpoints to LiveServ MS:
    PRECONDITIONS: Coral:
    PRECONDITIONS: * wss://liveserve-publisher-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - PROD
    PRECONDITIONS: * wss://liveserve-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - DEV0
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: * wss://liveserve-publisher-prd0.coralsports.prod.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - PROD
    PRECONDITIONS: * wss://liveserve-publisher-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - DEV0
    """
    keep_browser_open = True

    def test_001_tap_football_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap Football icon from the sports ribbon
        EXPECTED: * Football landing page is opened
        EXPECTED: * Websocket connection with LiveServeMS is established
        EXPECTED: * Subscription by IDs are sent to events that are present in the expanded competitions ONLY
        EXPECTED: * Match Result value is selected by default in the Market Selector
        """
        pass

    def test_002_choose_market_from_preconditions_in_the_market_selector_and_make_sure_that_only_one_event_with_particular_market_is_available_on_the_page(self):
        """
        DESCRIPTION: Choose market from Preconditions in the Market Selector and make sure that only ONE event with particular market is available on the page
        EXPECTED: * Selected Market is displayed in Market selector
        EXPECTED: * Only ONE event is displayed for selected market
        """
        pass

    def test_003_in_ti_tool_undisplay_selections_for_the_event_from_preconditions_and_save_changes(self):
        """
        DESCRIPTION: In TI tool undisplay selections for the event from preconditions and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_004_go_to_oxygen_application_and_verify_that_event_disappears_and_information_received_in_push(self):
        """
        DESCRIPTION: Go to Oxygen application and verify that event disappears and information received in push
        EXPECTED: * displayed:"N" attribute is received in WS
        EXPECTED: * event stops to display on the page in real time
        """
        pass

    def test_005_verify_market_selector(self):
        """
        DESCRIPTION: Verify Market Selector
        EXPECTED: * Chosen market stops to display within the Market selector
        EXPECTED: * Default value starts to display within the Market selector
        EXPECTED: * Events for default market starts to display on the page
        """
        pass

    def test_006_in_ti_tool_display_selections_for_the_event_from_preconditions_and_save_changes(self):
        """
        DESCRIPTION: In TI tool display selections for the event from preconditions and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_007_go_to_oxygen_application_and_verify_event_displaying_and_information_received_in_push(self):
        """
        DESCRIPTION: Go to Oxygen application and verify event displaying and information received in push
        EXPECTED: * displayed:"Y" attribute is received in WS
        EXPECTED: * event does NOT start to display in real time
        """
        pass

    def test_008_refresh_the_page_and_verify_the_event_displaying(self):
        """
        DESCRIPTION: Refresh the page and verify the event displaying
        EXPECTED: Event starts to display on the page
        """
        pass

    def test_009_verify_market_selector(self):
        """
        DESCRIPTION: Verify Market Selector
        EXPECTED: Market for event from the previous steps is visible within Market Selector
        """
        pass
