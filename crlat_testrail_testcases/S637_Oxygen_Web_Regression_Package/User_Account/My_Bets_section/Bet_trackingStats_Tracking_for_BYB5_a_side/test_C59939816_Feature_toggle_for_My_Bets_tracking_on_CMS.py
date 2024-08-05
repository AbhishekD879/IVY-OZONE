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
class Test_C59939816_Feature_toggle_for_My_Bets_tracking_on_CMS(Common):
    """
    TR_ID: C59939816
    NAME: Feature toggle for My Bets tracking on CMS
    DESCRIPTION: This test case verifies that subscription for updates is started on Football EDP and My Bets in case when BetTracking in enabled in CMS
    PRECONDITIONS: In Oxygen app
    PRECONDITIONS: * Create a Football event in OpenBet (T.I.)
    PRECONDITIONS: * Request Banach side to map data including Player Bets markets
    PRECONDITIONS: * Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: * Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: * Start recorded event (In TI set 'Іs Off' = yes)
    """
    keep_browser_open = True

    def test_001_navigate_to_cms___system_configuration___structure___bettracking(self):
        """
        DESCRIPTION: Navigate to CMS - System-configuration - Structure - BetTracking
        EXPECTED: 
        """
        pass

    def test_002_set_enabled__true_and_save_changes(self):
        """
        DESCRIPTION: Set **enabled** = **true** and save changes
        EXPECTED: Changes are saved
        """
        pass

    def test_003_navigate_to_oxygen_app___football_event_under_test_and_place_2_bets_on_byb_market(self):
        """
        DESCRIPTION: Navigate to Oxygen app - football event under test and place 2 bets on BYB market
        EXPECTED: Bets are placed successfully
        """
        pass

    def test_004_open_devtools___network_and_filter_by_web_sockets_ws(self):
        """
        DESCRIPTION: Open DevTools - Network and filter by Web Sockets (WS)
        EXPECTED: 
        """
        pass

    def test_005_open_my_bets_and_verify_previously_placed_bets_presence(self):
        """
        DESCRIPTION: Open My Bets and verify previously placed bets presence
        EXPECTED: Bets are present in My Bets
        """
        pass

    def test_006_verify_updates_subscription_open_eio3transportwebsocket_verify_42scoreboardeventid_message_presenceeg_42scoreboard10495498(self):
        """
        DESCRIPTION: Verify updates subscription:
        DESCRIPTION: * Open **EIO=3&transport=websocket**
        DESCRIPTION: * Verify **42["scoreboard","eventID"]** message presence
        DESCRIPTION: e.g. 42["scoreboard","10495498"]
        EXPECTED: **42["scoreboard","eventID"]** message is present and not duplicated (2 bets for same event have one subscription)
        """
        pass

    def test_007_navigate_to_settled_bets(self):
        """
        DESCRIPTION: Navigate to Settled bets
        EXPECTED: **42["unsubscribeScoreboard","eventID"]** message is present
        EXPECTED: e.g. 42["unsubscribeScoreboard","10495498"]
        """
        pass

    def test_008_navigate_to_cms___system_configuration___structure___bettracking_and_set_enabled__false(self):
        """
        DESCRIPTION: Navigate to CMS - System-configuration - Structure - BetTracking and set **enabled** = **false**
        EXPECTED: 
        """
        pass

    def test_009_open_oxygen_app___my_bets_and_open_eio3transportwebsocket_in_devtools(self):
        """
        DESCRIPTION: Open Oxygen app - My Bets and open **EIO=3&transport=websocket** in DevTools
        EXPECTED: - **42["scoreboard","eventID"]** message is not present
        EXPECTED: - progress bar, stats description field and winning/ losing indicator in the left hand grey bar are **not displayed**
        """
        pass
