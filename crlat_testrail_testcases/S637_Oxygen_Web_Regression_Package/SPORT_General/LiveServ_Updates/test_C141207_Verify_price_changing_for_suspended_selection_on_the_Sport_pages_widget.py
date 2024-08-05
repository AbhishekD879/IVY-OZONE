import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C141207_Verify_price_changing_for_suspended_selection_on_the_Sport_pages_widget(Common):
    """
    TR_ID: C141207
    NAME: Verify price changing for suspended selection on the <Sport> pages/widget
    DESCRIPTION: This test case verifies price changing for suspended selection on the <Sport> pages/widget
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: **Updates are received via push notifications on EDP**
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

    def test_002_navigate_to_sports_landing_page_from_sports_ribbonleft_navigation_menu(self):
        """
        DESCRIPTION: Navigate to Sports Landing page from Sports Ribbon/Left Navigation menu
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_003___open_matches_today_tab_for_desktop__open_matches_tab_for_mobile(self):
        """
        DESCRIPTION: - Open 'Matches'->'Today' tab (for desktop)
        DESCRIPTION: - Open 'Matches' tab (for mobile)
        EXPECTED: * 'Matches' page is opened
        EXPECTED: * Websocket connection with LiveServeMS is established
        EXPECTED: * Subscription by IDs are sent to events that are present in the expanded competitions ONLY
        """
        pass

    def test_004_verify_the_priceodds_buttons_view_of_the_events_displayed(self):
        """
        DESCRIPTION: Verify the 'Price/Odds' buttons view of the events displayed
        EXPECTED: 'Price/Odds' buttons display price received from backend on light grey background
        """
        pass

    def test_005_trigger_the_following_situation_for_any_outcomeeventstatuscodesand_at_the_same_time_have_sport_landing_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for any outcome:
        DESCRIPTION: eventStatusCode="S"
        DESCRIPTION: and at the same time have <Sport> Landing page opened to watch for updates
        EXPECTED: 
        """
        pass

    def test_006_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: * Update is received in WS with **type="sEVENT"**
        EXPECTED: * Price/Odds button for selected outcome is displayed immediately as greyed out and become disabled on <Sport> Landing page
        EXPECTED: * Price is still displaying on the Price/Odds button
        """
        pass

    def test_007_trigger_price_change_for_suspended_outcome__from_the_current_page(self):
        """
        DESCRIPTION: Trigger price change for suspended outcome  from the current page
        EXPECTED: 
        """
        pass

    def test_008_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: * Update is received in WS with **type="sEVENT"**
        EXPECTED: * Corresponding 'Price/Odds' button immediately displays new prices
        EXPECTED: * Price/Odds' button doesn't change the color (to blue color if price has decreased or to
        EXPECTED: red color if price has increased)
        """
        pass

    def test_009_change_attribute_for_this_outcomeeventstatuscodeaand_at_the_same_time_have_sport_landing_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Change attribute for this outcome:
        DESCRIPTION: eventStatusCode="A"
        DESCRIPTION: and at the same time have <Sport> Landing page opened to watch for updates
        EXPECTED: 
        """
        pass

    def test_010_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: * Update is received in WS with **type="sEVENT"**
        EXPECTED: * Price/Odds button for selected outcome is no more disabled, it becomes active immediately
        """
        pass

    def test_011_repeat_steps_1_10_for_sport_in_play_page(self):
        """
        DESCRIPTION: Repeat steps 1-10 for <Sport> In-Play page
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_1_10_for_sport_event_detailes_page(self):
        """
        DESCRIPTION: Repeat steps 1-10 for <Sport> Event Detailes page
        EXPECTED: * Updates are received via push notifications
        """
        pass

    def test_013_for_desktopnavigate_to_sports_landing_page_make_sure_that_sport_has_available_live_events_from_sports_ribbonleft_navigation_menu(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page (make sure that Sport has available live events) from Sports Ribbon/Left Navigation menu
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * 'Matches' tab is selected by default
        EXPECTED: * In-Play widget with available live events for particular Sport is displayed in 3-rd Service column
        EXPECTED: * Live Stream widget is displayed below In-Play widget (in case in-play event has streaming mapped)
        """
        pass

    def test_014_for_desktoprepeat_steps_4_10_for_in_play_and_live_stream_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 4-10 for In-Play and Live Stream widget
        EXPECTED: 
        """
        pass

    def test_015_for_desktopnavigate_to_in_play__live_stream_section_at_the_homepage_by_scrolling_the_page_down(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section at the Homepage by scrolling the page down
        EXPECTED: * Two switchers are visible: 'In-Play' and 'Live Stream'
        EXPECTED: * 'In-Play' is default one
        """
        pass

    def test_016_for_desktoprepeat_steps_4_10_for_both_in_play_and_live_stream_switchers(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 4-10 for both 'In-Play' and 'Live Stream' switchers
        EXPECTED: 
        """
        pass
