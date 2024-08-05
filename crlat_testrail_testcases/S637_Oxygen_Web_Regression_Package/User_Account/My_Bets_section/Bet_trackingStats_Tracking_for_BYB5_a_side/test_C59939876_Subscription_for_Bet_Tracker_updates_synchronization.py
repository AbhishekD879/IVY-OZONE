import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C59939876_Subscription_for_Bet_Tracker_updates_synchronization(Common):
    """
    TR_ID: C59939876
    NAME: Subscription for Bet Tracker updates synchronization
    DESCRIPTION: This test case verifies that subscription for Bet Tracker updates stays open after closing one of two available "My Bets" tabs
    PRECONDITIONS: In Oxygen app
    PRECONDITIONS: * Create a Football event in OpenBet (T.I.)
    PRECONDITIONS: * Request Banach side to map data including Player Bets markets
    PRECONDITIONS: * Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: * Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: * Start recorded event (In TI set 'Іs Off' = yes)
    PRECONDITIONS: * Place BYB bet on event under test
    PRECONDITIONS: * CMS - System-configuration - Structure - BetTracking enabled = true
    """
    keep_browser_open = True

    def test_001_in_oxygen_app_navigate_to_open_bets_and_open_my_bets_in_widget(self):
        """
        DESCRIPTION: In Oxygen app navigate to /open-bets and open My Bets in widget
        EXPECTED: 
        """
        pass

    def test_002_open_devtools___network_and_filter_by_web_sockets_ws_verify_subscription_for_bet_tracker_updates(self):
        """
        DESCRIPTION: Open DevTools - Network and filter by Web Sockets (WS), verify subscription for Bet Tracker updates
        EXPECTED: **42["scoreboard","eventID"]** message is present
        EXPECTED: ![](index.php?/attachments/get/119867083)
        """
        pass

    def test_003_navigate_to_football_landing_pageopen_bets_tab_in_widget_is_still_opened(self):
        """
        DESCRIPTION: Navigate to football landing page
        DESCRIPTION: (Open Bets tab in widget is still opened)
        EXPECTED: **42["unsubscribeScoreboard","eventID"]** message does not appear in
        EXPECTED: **?EIO=3&transport=websocket**
        """
        pass

    def test_004_click_betslip_in_open_bets_widget(self):
        """
        DESCRIPTION: Click Betslip in open-bets widget
        EXPECTED: **42["unsubscribeScoreboard","eventID"]** message appears in
        EXPECTED: **?EIO=3&transport=websocket**
        """
        pass

    def test_005_navigate_to_test_football_events_edp_and_click_my_bets(self):
        """
        DESCRIPTION: Navigate to test football event's EDP and click **My Bets**
        EXPECTED: **42["scoreboard","eventID"]** message appears in
        EXPECTED: **?EIO=3&transport=websocket**
        EXPECTED: ![](index.php?/attachments/get/120241353)
        """
        pass

    def test_006_in_widget_click_my_bets___open_bets(self):
        """
        DESCRIPTION: In widget click **My Bets - Open Bets**
        EXPECTED: 
        """
        pass

    def test_007_on_edp_click_markets_tab(self):
        """
        DESCRIPTION: On EDP click Markets tab
        EXPECTED: **42["unsubscribeScoreboard","eventID"]** message does not appear in
        EXPECTED: **?EIO=3&transport=websocket**
        """
        pass
