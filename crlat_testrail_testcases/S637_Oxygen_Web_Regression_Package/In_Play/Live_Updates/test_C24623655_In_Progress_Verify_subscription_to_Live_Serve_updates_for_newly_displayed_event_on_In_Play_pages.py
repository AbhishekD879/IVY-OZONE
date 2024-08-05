import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C24623655_In_Progress_Verify_subscription_to_Live_Serve_updates_for_newly_displayed_event_on_In_Play_pages(Common):
    """
    TR_ID: C24623655
    NAME: [In Progress] Verify subscription to Live Serve updates for newly displayed event on 'In-Play' pages
    DESCRIPTION: This test case verifies subscription to Live Serve updates for newly displayed event on 'In-Play' pages
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon **Mobile/Tablet** or 'Main Navigation' menu at the 'Universal Header' (**Desktop**) and choose any Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section **Mobile/Tablet** or when 'Live Now' switcher is selected **Desktop**
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section **Mobile/Tablet** or select 'Upcoming' switcher **Desktop**
    PRECONDITIONS: **Note!** To check Live Serv notifications open Dev tools -> Network tab -> WS tab -> Frames section -> choose **?EIO=3&transport=websocket** record
    PRECONDITIONS: Unsubscription from Live updates when the event is undisplayed:
    PRECONDITIONS: ![](index.php?/attachments/get/40874)
    """
    keep_browser_open = True

    def test_001_verify_subscription_for_expanded_sport_competitions(self):
        """
        DESCRIPTION: Verify subscription for expanded <Sport> competitions
        EXPECTED: * Only events from expanded <Sport> competition are subscribed to Live Serv updates
        EXPECTED: 42["subscribe", [<eventId>, <eventId>...] is received in WS
        EXPECTED: * There is no subscription for events from collapsed <Sport>categories /<Sport> competition
        """
        pass

    def test_002_undisplay_any_event_from_expanded_sportcompetition_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Undisplay any event from expanded <Sport>competition in Openbet TI tool
        EXPECTED: * Update is received in WS:
        EXPECTED: 42["eventID",{"publishedDate":<date>,"type":<type>...
        EXPECTED: for event: type: "EVENT"
        """
        pass

    def test_003_trigger_any_updates_for_the_undisplayed_event_in_openbet_ti_tool_eg_price_change_suspend(self):
        """
        DESCRIPTION: Trigger any updates for the undisplayed event in Openbet TI tool (e.g. price change, suspend)
        EXPECTED: * Update is not received in WS
        """
        pass

    def test_004_(self):
        """
        DESCRIPTION: 
        EXPECTED: 
        """
        pass

    def test_005_collapse_expanded_sport_competition(self):
        """
        DESCRIPTION: Collapse expanded <Sport> competition
        EXPECTED: * Events in this category are unsubscribed from updates:
        EXPECTED: 42["unsubscribe", [<eventId>, <eventId>...]
        """
        pass

    def test_006_navigate_to_watch_live_tab_on_in_play_page_repeat_steps_1_4(self):
        """
        DESCRIPTION: Navigate to 'Watch Live' tab on 'In-Play' page repeat steps 1-4
        EXPECTED: 
        """
        pass

    def test_007_expand_collapsed_sport_category(self):
        """
        DESCRIPTION: Expand collapsed <Sport> category
        EXPECTED: * Loading icon is displayed until all events from current <Sport> will be loaded
        EXPECTED: * 42 ["subscribe", "IN_PLAY_SPORT_COMPETITION_CHANGED::<category_id>::LIVE_EVENT"]  record received in WS for only for expanded competitions
        EXPECTED: * Only events from expanded <Sport> competition are subscribed to Live Serv updates
        EXPECTED: 42["subscribe", [<eventId>, <eventId>...] is received in WS
        EXPECTED: * There is no subscription for events from collapsed <Sport> competition
        """
        pass

    def test_008_update_any_eventmarketselection_from_just_expanded_sport_in_openbet_ti_tool_eg_price_change_suspend(self):
        """
        DESCRIPTION: Update any event/market/selection from just expanded <Sport> in Openbet TI tool (e.g. price change, suspend)
        EXPECTED: * Update is received in WS:
        EXPECTED: 42["eventID",{"publishedDate":<date>,"type":<type>...
        EXPECTED: for market: type: "EVMKT"
        EXPECTED: for event: type: "EVENT"
        EXPECTED: for selection: type: "SELCN"
        EXPECTED: for price: type: "PRICE"
        """
        pass

    def test_009_collapse_expanded_sport_category(self):
        """
        DESCRIPTION: Collapse expanded <Sport> category
        EXPECTED: * Events from all competitions that were expanded and subscribed are unsubscribed from updates:
        EXPECTED: 42["unsubscribe", [<eventId>, <eventId>...]
        EXPECTED: * 42["unsubscribe", "IN_PLAY_SPORT_COMPETITION_CHANGED::<category_id>::LIVE_EVENT"] received in WS
        """
        pass

    def test_010_go_to_upcoming_section_and_repeat_steps_3_8(self):
        """
        DESCRIPTION: Go to 'Upcoming' section and repeat steps 3-8
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_1_9_for_the_following_pages_home_page__in_play_tab_mobiletablet_sports_landing_page__in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-9 for the following pages:
        DESCRIPTION: * Home page > 'In-Play' tab **Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        EXPECTED: 
        """
        pass

    def test_012_desktop_home_page_for_in_play__live_stream_section_for_both_switchers_sport_landing_page_for_in_play_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: * Home page for 'In-play & Live Stream' section for both switchers
        DESCRIPTION: * Sport Landing page for 'In-play' widget
        EXPECTED: 
        """
        pass
