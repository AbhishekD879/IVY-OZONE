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
class Test_C356714_Verify_hiding_Events_depending_on_Displayed_attribute_for_selections(Common):
    """
    TR_ID: C356714
    NAME: Verify hiding Events depending on 'Displayed' attribute for selections
    DESCRIPTION: This test case verifies hiding Events depending on 'Displayed' attribute for selections
    PRECONDITIONS: 1. To display/undisplay event/market/selection use http://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. Events should have the following attributes:
    PRECONDITIONS: *   drilldownTagNames="EVFLAG_BL" - Bet in Play List check in TI on the event level
    PRECONDITIONS: *   isMarketBetInRun = "true" - Bet In Run check in TI on the market level
    PRECONDITIONS: To check updates open Dev Tools -> Network tab -> WS option
    PRECONDITIONS: Endpoints to LiveServ MS:
    PRECONDITIONS: Coral:
    PRECONDITIONS: * wss://liveserve-publisher-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - PROD
    PRECONDITIONS: * wss://liveserve-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - DEV0
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: * wss://liveserve-publisher-prd0.coralsports.prod.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - PROD
    PRECONDITIONS: * wss://liveserve-publisher-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - DEV0
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_tap_football_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap Football icon from the sports ribbon
        EXPECTED: * Football landing page is opened
        EXPECTED: * 'Today' tab is selected (for desktop)/'Matches' tab is opened (for mobile)
        EXPECTED: * Events for current day are displayed
        EXPECTED: * Match Result value is selected by default in the Market Selector
        EXPECTED: * Websocket connection with LiveServeMS is established
        EXPECTED: * Subscription by IDs are sent to events that are present in the expanded competitions ONLY
        """
        pass

    def test_003_choose_any_market_different_from_match_result_in_the_market_selector_and_make_sure_that_only_one_event_is_available_on_the_page(self):
        """
        DESCRIPTION: Choose any market different from Match Result in the Market Selector and make sure that only ONE event is available on the page
        EXPECTED: * Selected Market is displayed in Market selector
        EXPECTED: * Only ONE event is displayed for selected market
        """
        pass

    def test_004_in_ti_tool_undisplay_selections_for_the_event_from_step_3_and_save_changes(self):
        """
        DESCRIPTION: In TI tool undisplay selections for the event from step 3 and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_005_go_to_oxygen_application_and_verify_information_received_in_push(self):
        """
        DESCRIPTION: Go to Oxygen application and verify information received in push
        EXPECTED: displayed:"N" attribute is received in WS
        """
        pass

    def test_006_verify_event_and_market_selector_displaying(self):
        """
        DESCRIPTION: Verify event and market selector displaying
        EXPECTED: * Chosen market stops to display within the Market selector
        EXPECTED: * Default value starts to display within the Market selector
        EXPECTED: * Events for default market starts to display on the page
        """
        pass

    def test_007_in_ti_tool_display_selections_for_the_event_from_step_3_and_save_changes(self):
        """
        DESCRIPTION: In TI tool display selections for the event from step 3 and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_008_go_to_oxygen_application_and_verify_information_received_in_push(self):
        """
        DESCRIPTION: Go to Oxygen application and verify information received in push
        EXPECTED: displayed:"Y" attribute is received in WS
        """
        pass

    def test_009_verify_event_and_market_selector_displaying(self):
        """
        DESCRIPTION: Verify event and market selector displaying
        EXPECTED: * Default market is still displayed within Market Selector
        EXPECTED: * event does NOT start to display in real time
        """
        pass

    def test_010_refresh_the_page_and_verify_displaying_market_from_step_3(self):
        """
        DESCRIPTION: Refresh the page and verify displaying market from step 3
        EXPECTED: Market from step 3 is visible within Market Selector
        """
        pass

    def test_011_repeat_steps_3_10_for_tomorrowfuture_eventsfuture_events_are_shown_only_on_desktop(self):
        """
        DESCRIPTION: Repeat steps 3-10 for Tomorrow/Future events
        DESCRIPTION: *Future events are shown only on Desktop*
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_3_10_for_competitions_detailed_page(self):
        """
        DESCRIPTION: Repeat steps 3-10 for Competitions Detailed page
        EXPECTED: 
        """
        pass
