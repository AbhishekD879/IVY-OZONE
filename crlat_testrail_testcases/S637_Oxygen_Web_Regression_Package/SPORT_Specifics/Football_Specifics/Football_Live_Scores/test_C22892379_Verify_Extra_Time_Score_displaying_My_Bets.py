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
class Test_C22892379_Verify_Extra_Time_Score_displaying_My_Bets(Common):
    """
    TR_ID: C22892379
    NAME: Verify Extra Time Score displaying (My Bets)
    DESCRIPTION: This test case verifies Extra Time Score displaying on My Bets>Open Bets, Cashout?, Settled bets
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * Event is created in Amelco;
    PRECONDITIONS: * Event is in Main Time;
    PRECONDITIONS: * Live Scores are added to this Event within Main Time;
    PRECONDITIONS: * In Play events have attribute drilldownTagNames = EVFLAG_BL ('Bet In Play list' check box in ti) where: live now: start time in the past ( but less than 1 day), isOff = Yes (in siteSetver in isLiveNowEvent=true, isStarted = true)
    PRECONDITIONS: Extra-time markets should already be displayed, unsuspended and priced before step #4
    PRECONDITIONS: NOTE: In order to have live scores, the event has to be configured in Amelco https://confluence.egalacoral.com/display/SPI/Amelco+Systems . Scores can be changed in the same tool.
    PRECONDITIONS: Instruction: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    PRECONDITIONS: * User should place a bet on this in play event
    PRECONDITIONS: wss://liveserve-publisher-prd0.coralsports.prod.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket
    """
    keep_browser_open = True

    def test_001_navigate_to_my_betsopn_betscashout_tab(self):
        """
        DESCRIPTION: Navigate to My Bets>Opn Bets/Cashout tab
        EXPECTED: Placed bet is shown
        """
        pass

    def test_002_verify_live_scores_values_for_the_corresponding_event_within_main_time(self):
        """
        DESCRIPTION: Verify Live Scores values for the corresponding Event (within Main Time)
        EXPECTED: Live Scores are showing for the Event
        """
        pass

    def test_003_check_live_scores_updates_via_ws_main_time(self):
        """
        DESCRIPTION: Check Live Scores updates via WS (Main Time)
        EXPECTED: Live Scores values match with the ones set via Amelco (live Score updates are sent via WS -> wss://liveserve-publisher-prd0.coralsports.prod.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket -> "type":"SCBRD"
        """
        pass

    def test_004_set_event_to_extra_time_via_amelcochange_score_for_team_1verify_updated_scores_displaying_in_application(self):
        """
        DESCRIPTION: Set Event to Extra Time via Amelco
        DESCRIPTION: Change score for Team 1
        DESCRIPTION: Verify updated scores displaying in application
        EXPECTED: * Score immediately starts displaying new value for Team 1
        EXPECTED: * Extra Time Score value is added to Main Time Score value and displaying as **Main Time Score + Extra Time Score**
        """
        pass

    def test_005_verify_score_update_receiving_via_ws(self):
        """
        DESCRIPTION: Verify Score update receiving via WS
        EXPECTED: * Live Scores values match with the ones set via Amelco (live Score updates are sent via WS -> wss://liveserve-publisher-prd0.coralsports.prod.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket -> "type":"SCBRD"
        EXPECTED: * New property extraTimeScore:"X" is added to comments.teams ("IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX") and is displaying correct Live Score value set within Extra Time
        """
        pass

    def test_006_change_score_for_team_2_event_is_in_extra_timeverify_updated_scores_displaying_in_application(self):
        """
        DESCRIPTION: Change score for Team 2 (Event is in Extra Time)
        DESCRIPTION: Verify updated scores displaying in application
        EXPECTED: * Score immediately starts displaying new value for Team 1
        EXPECTED: * Extra Time Score value is added to Main Time Score value and displaying as **Main Time Score + Extra Time Score**
        """
        pass

    def test_007_verify_score_update_receiving_via_ws(self):
        """
        DESCRIPTION: Verify Score update receiving via WS
        EXPECTED: * Live Scores values match with the ones set via Amelco (live Score updates are sent via WS -> wss://liveserve-publisher-prd0.coralsports.prod.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket -> "type":"SCBRD"
        EXPECTED: * New property extraTimeScore:"X" is added to comments.teams ("IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX") and is displaying correct Live Score value set within Extra Time
        """
        pass
