import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2064780_Verify_Live_Scores_updates(Common):
    """
    TR_ID: C2064780
    NAME: Verify Live Scores updates
    DESCRIPTION: This test case verifies Live Scores/ Match Time Updates within coupon
    DESCRIPTION: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    PRECONDITIONS: *   Valid Cash Out Coupon Code should be generated with Live Scores available (support is needed from RCOMB team)
    PRECONDITIONS: *   Commentary data is available only for started events
    PRECONDITIONS: *   To find all details related to the coupon open browser console (F12) -> Network -> request 'coupon?id=<coupon code>' -> Preview
    PRECONDITIONS: *   To find details about live scores in Preview tab of 'coupon?id=<coupon code>' request expand the following elements : bet -> leg -> sportsLeg -> legPart -> eventParticipants/eventPeriod
    PRECONDITIONS: In order to get events with Scorers use link, where XXX - event id:
    PRECONDITIONS: http://backoffice-tst2.coralbip.co.uk/openbet-ssviewer/Commentary/2.15/CommentaryForEvent/XXX
    PRECONDITIONS: Look at the attributes to know correct score:
    PRECONDITIONS: *   **eventParticipantID** -  to verify team name and corresponding team score
    PRECONDITIONS: *   **periodCode**='ALL' & **description**="Total Duration of the game/match' - to look at the scorers for the full match
    PRECONDITIONS: *   **factCode**='SCORE' &** name**='Score of the match/game' - to see Match facts
    PRECONDITIONS: *   **'fact'** - to see a score for particular participant
    PRECONDITIONS: *   **'roleCode' - **HOME/AWAY to see home and away team.
    PRECONDITIONS: * All live updates are coming through WebSockets
    PRECONDITIONS: ** Events score/time can be managed in ATS Amelco **
    PRECONDITIONS: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    """
    keep_browser_open = True

    def test_001__load_sportbook_app_log_in_chose_connect_from_header_ribbon_select_shop_bet_tracker(self):
        """
        DESCRIPTION: * Load Sportbook App
        DESCRIPTION: * Log in
        DESCRIPTION: * Chose 'Connect' from header ribbon
        DESCRIPTION: * Select 'Shop Bet Tracker'
        EXPECTED: Bet Tracker page is opened
        """
        pass

    def test_002_submit_valid_cash_out_code_which_containspre_play_event(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains pre-play event
        EXPECTED: *   Cash Out Code is submitted successfully
        EXPECTED: *   Cash Out Coupon is shown to the user expanded by default
        EXPECTED: *   Score is not displayed
        """
        pass

    def test_003_trigger_event_kick_off(self):
        """
        DESCRIPTION: Trigger event kick-off
        EXPECTED: *   Event is started
        EXPECTED: *   Score 0 : 0 is displayed (from the right of event name)
        """
        pass

    def test_004_trigger_score_changes(self):
        """
        DESCRIPTION: Trigger score changes
        EXPECTED: * New score is mirrored on interface immediately
        EXPECTED: * Score corresponds to the** 'fact'** attribute from the SS on periodCode="**ALL**" level
        EXPECTED: * Score for the **Home **team is shown near home team name
        EXPECTED: roleCode="HOME"
        EXPECTED: * Score for the **Away **team is shown near away team name roleCode="AWAY"
        EXPECTED: Note: use **eventParticipantId **for matching Team and Score
        """
        pass

    def test_005_submit_valid_cash_out_code_which_containselection_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contain selection which doesn't have Live Score available
        EXPECTED: *   Only 'LIVE' label is shown (instead of Score)
        EXPECTED: *   Match Time is not shown
        EXPECTED: *   The Sports icon is displayed only
        """
        pass

    def test_006_go_to_my_bets__in_shop_bets_sub_tub__repeat_steps_3_5(self):
        """
        DESCRIPTION: Go to 'My Bets' ->'In-Shop Bets' sub-tub ->
        DESCRIPTION: repeat steps #3-5
        EXPECTED: 
        """
        pass
