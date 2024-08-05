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
class Test_C2696914_Event_Market_Selection_becomes_Suspended_Active_on_Future_tab_of_Sport_Landing_page(Common):
    """
    TR_ID: C2696914
    NAME: Event/Market/Selection becomes Suspended/Active on Future tab of <Sport> Landing page
    DESCRIPTION: This test case verifies suspension/unsuspension on Future tab of <Sport> Landing page
    PRECONDITIONS: There are <Sport> Future events
    PRECONDITIONS: Events should have the following attributes:
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

    def test_001___open_future_tab_of_sport_landing_page_desktop_only(self):
        """
        DESCRIPTION: - Open Future tab of <Sport> Landing page (desktop only)
        EXPECTED: * Future tab is selected (for desktop)
        EXPECTED: * Websocket connection with LiveServeMS is established
        EXPECTED: * Subscription by IDs are sent to events that are present in the expanded competitions ONLY
        """
        pass

    def test_002_trigger_the_following_situation_for_the_future_eventeventstatuscodes__and_at_the_same_time_have_future_tab_opened_to_watch_for_updates_for_desktop__and_at_the_same_time_have_matches_tab_opened_to_watch_for_updates_for_mobile(self):
        """
        DESCRIPTION: Trigger the following situation for the future event:
        DESCRIPTION: **eventStatusCode="S"**
        DESCRIPTION: - and at the same time have Future tab opened to watch for updates (for desktop)
        DESCRIPTION: - and at the same time have Matches tab opened to watch for updates (for mobile)
        EXPECTED: * Update is received in WS with **type="sEVENT"**
        """
        pass

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: Price/Odds buttons of this event are displayed immediately as greyed out and become disabled but still displaying the prices
        """
        pass

    def test_004_change_attribute_for_this_eventeventstatuscodea__and_at_the_same_time_have_future_tab_opened_to_watch_for_updates_for_desktop__and_at_the_same_time_have_matches_tab_opened_to_watch_for_updates_for_mobile(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **eventStatusCode="A" **
        DESCRIPTION: - and at the same time have Future tab opened to watch for updates (for desktop)
        DESCRIPTION: - and at the same time have Matches tab opened to watch for updates (for mobile)
        EXPECTED: * Update is received in WS with **type="sEVENT"**
        EXPECTED: * All Price/Odds buttons of this event are no more disabled, they become active immediately
        """
        pass

    def test_005_collapse_competition_and_trigger_suspension_for_event(self):
        """
        DESCRIPTION: Collapse competition and trigger suspension for event
        EXPECTED: * Unsubscription by IDs are sent to events that are present in collapsed competitions ONLY
        EXPECTED: * Event suspension update is NOT received in WS
        """
        pass

    def test_006_expand_competition_and_verify_event_suspension(self):
        """
        DESCRIPTION: Expand competition and verify event suspension
        EXPECTED: * Subscription by IDs are sent again to event in the expanded competition
        EXPECTED: * Event suspension update is received in WS
        EXPECTED: * Price/Odds buttons of this event are displayed immediately as greyed out
        """
        pass

    def test_007_repeat_steps_2_6_for_suspension_on_market_levelmarketstatuscodesmarketstatuscodea(self):
        """
        DESCRIPTION: Repeat steps 2-6 for Suspension on Market level:
        DESCRIPTION: **marketStatusCode="S"**
        DESCRIPTION: **marketStatusCode="A"**
        EXPECTED: * Update is received in WS with **type="sEVMKT"**
        """
        pass

    def test_008_repeat_steps_2_6_for_suspension_on_selection_leveloutcomestatuscodesoutcomestatuscodea(self):
        """
        DESCRIPTION: Repeat steps 2-6 for Suspension on selection level:
        DESCRIPTION: **outcomeStatusCode="S"**
        DESCRIPTION: **outcomeStatusCode="A"**
        EXPECTED: * Update is received in WS with **type="sSELCN"**
        """
        pass
