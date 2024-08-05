import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C440556_Verify_subscription_to_Live_Serve_updates_on_In_Play(Common):
    """
    TR_ID: C440556
    NAME: Verify subscription to Live Serve updates on In Play
    DESCRIPTION: This test case verifies subscription to Live Serv updates on In Play page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon **Mobile/Tablet** or 'Main Navigation' menu at the 'Universal Header' (**Desktop**) and choose any Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section **Mobile/Tablet** or when 'Live Now' switcher is selected **Desktop**
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section **Mobile/Tablet** or select 'Upcoming' switcher **Desktop**
    PRECONDITIONS: **Note!** To check Live Serv notifications open Dev tools -> Network tab -> WS tab -> Frames section -> choose **?EIO=3&transport=websocket** record
    PRECONDITIONS: Subscription to live updates:
    PRECONDITIONS: ![](index.php?/attachments/get/40864)
    PRECONDITIONS: Unsubscription from live updates:
    PRECONDITIONS: ![](index.php?/attachments/get/40868)
    PRECONDITIONS: Updates for subscribed event:
    PRECONDITIONS: ![](index.php?/attachments/get/40866)
    """
    keep_browser_open = True

    def test_001_verify_subscription_for_expanded_sporttype_accordions(self):
        """
        DESCRIPTION: Verify subscription for expanded <Sport/Type> accordions
        EXPECTED: * Only events from expanded <Sport/Type> accordions are subscribed to Live Serv updates
        EXPECTED: 42["subscribe", [<eventId>, <eventId>...] is received in WS
        EXPECTED: * There is no subscription for events from collapsed <Sport/Type> accordions
        """
        pass

    def test_002_update_any_eventmarketselection_from_expanded_sporttype_accordion_in_openbet_ti_tool_eg_price_change_suspend(self):
        """
        DESCRIPTION: Update any event/market/selection from expanded <Sport/Type> accordion in Openbet TI tool (e.g. price change, suspend)
        EXPECTED: * Update is received in WS:
        EXPECTED: 42["eventID",{"publishedDate":<date>,"type":<type>...
        EXPECTED: for market: type: "EVMKT"
        EXPECTED: for event: type: "EVENT"
        EXPECTED: for selection: type: "SELCN"
        EXPECTED: for price: type: "PRICE"
        """
        pass

    def test_003_update_any_eventmarketselection_from_collapsed_sporttype_accordion_in_openbet_ti_tool_eg_price_change_suspend(self):
        """
        DESCRIPTION: Update any event/market/selection from collapsed <Sport/Type> accordion in Openbet TI tool (e.g. price change, suspend)
        EXPECTED: * Update is not received in WS
        """
        pass

    def test_004_collapse_expanded_sporttype_accordion(self):
        """
        DESCRIPTION: Collapse expanded <Sport/Type> accordion
        EXPECTED: * Events in this <Sport/Type> accordion are unsubscribed from updates:
        EXPECTED: 42["unsubscribe", [<eventId>, <eventId>...]
        """
        pass

    def test_005_navigate_to_watch_live_tab_on_in_play_page_repeat_steps_1_4(self):
        """
        DESCRIPTION: Navigate to 'Watch Live' tab on 'In-Play' page repeat steps 1-4
        EXPECTED: 
        """
        pass

    def test_006_expand_collapsed_sporttype_accordions(self):
        """
        DESCRIPTION: Expand collapsed <Sport/Type> accordions
        EXPECTED: * Loading icon is displayed until all events from current <Sport> will be loaded
        EXPECTED: * 42 ["subscribe", "IN_PLAY_SPORT_COMPETITION_CHANGED::<category_id>::LIVE_EVENT"]  record received in WS for only for expanded competitions
        EXPECTED: * Only events from expanded <Sport/Type> accordions are subscribed to Live Serv updates
        EXPECTED: 42["subscribe", [<eventId>, <eventId>...] is received in WS
        EXPECTED: * There is no subscription for events from collapsed <Sport/Type> accordions
        """
        pass

    def test_007_update_any_eventmarketselection_from_just_expanded_sporttype_accordions_in_openbet_ti_tool_eg_price_change_suspend(self):
        """
        DESCRIPTION: Update any event/market/selection from just expanded <Sport/Type> accordions in Openbet TI tool (e.g. price change, suspend)
        EXPECTED: * Update is received in WS:
        EXPECTED: 42["eventID",{"publishedDate":<date>,"type":<type>...
        EXPECTED: for market: type: "EVMKT"
        EXPECTED: for event: type: "EVENT"
        EXPECTED: for selection: type: "SELCN"
        EXPECTED: for price: type: "PRICE"
        """
        pass

    def test_008_collapse_expanded_sporttype_accordion(self):
        """
        DESCRIPTION: Collapse expanded <Sport/Type> accordion
        EXPECTED: * Events from all competitions that were expanded and subscribed are unsubscribed from updates:
        EXPECTED: 42["unsubscribe", [<eventId>, <eventId>...]
        EXPECTED: * 42["unsubscribe", "IN_PLAY_SPORT_COMPETITION_CHANGED::<category_id>::LIVE_EVENT"] received in WS
        """
        pass

    def test_009_go_to_upcoming_section_and_repeat_steps_3_8(self):
        """
        DESCRIPTION: Go to 'Upcoming' section and repeat steps 3-8
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_1_9_for_the_following_pages_home_page__in_play_tab_mobiletablet_sports_landing_page__in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-9 for the following pages:
        DESCRIPTION: * Home page > 'In-Play' tab **Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        EXPECTED: 
        """
        pass

    def test_011_desktop_home_page_for_in_play__live_stream_section_for_both_switchers_sport_landing_page_for_in_play_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: * Home page for 'In-play & Live Stream' section for both switchers
        DESCRIPTION: * Sport Landing page for 'In-play' widget
        EXPECTED: 
        """
        pass
