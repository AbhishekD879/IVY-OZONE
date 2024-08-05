import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C1489740_Verify_Basketball_Live_Scores_in_My_Bets_section(Common):
    """
    TR_ID: C1489740
    NAME: Verify Basketball Live Scores in 'My Bets' section
    DESCRIPTION: This test case verifies Basketball Live Scores on 'Cash Out', 'Open Bets' and 'Bet History' tabs
    PRECONDITIONS: * User should be logged in to see their cash out/open bets/bet history
    PRECONDITIONS: * User should have placed bets on a Bsketball live event with scores available
    PRECONDITIONS: 1) In order to have a Scores Basketball event should be in-play
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: **participant_id** -  to verify team name and corresponding team score
    PRECONDITIONS: **period_code='ALL'** - to look at the scorers for the full match
    PRECONDITIONS: **period_code='QUARTER'** - to look at the scorers for the the specific time
    PRECONDITIONS: **period_index='1/2/3/4'** - to identify the particular 'QUARTER'
    PRECONDITIONS: **code='SCORE'**
    PRECONDITIONS: **value** - to see a score for the particular participant
    PRECONDITIONS: **role_code - 'TEAM_1'/'TEAM_2' or 'HOME'/'AWAY'** - to see home and away team
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: roleCode - 'TEAM_1'/'TEAM_2'
    PRECONDITIONS: PROD: roleCode - 'HOME/'AWAY'
    PRECONDITIONS: 3) Use the following link for verification SS commentary response http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: *NOTE:*
    PRECONDITIONS: 1) Use https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Amelco+Systems in order to generate live scores for BIP event.
    PRECONDITIONS: 2) If in the SiteServer commentary response the event has a typeFlagCode ="US" the scores should be displayed in reverse order i.e. away score first and home score last.
    PRECONDITIONS: 3) We received all score information, but no clock or period information. This means that the only period stored within OB is the "ALL" period, and so all 'values' are stored against this period.
    """
    keep_browser_open = True

    def test_001_go_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Go to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: * Cash out page is opened
        EXPECTED: * User's cash out bets are shown
        """
        pass

    def test_002_verify_basketball_bet_with_scores_available(self):
        """
        DESCRIPTION: Verify 'Basketball' bet with scores available
        EXPECTED: * The bet is shown in the cash out section
        EXPECTED: * Live scores are displayed
        EXPECTED: * 'LIVE' label is displayed
        """
        pass

    def test_003_verify_score_displaying(self):
        """
        DESCRIPTION: Verify score displaying
        EXPECTED: Scores are shown in the following format:
        EXPECTED: **FOR** **RELEASE** **99**
        EXPECTED: <Event name> <Team 1 score> <Team 2 score> <"LIVE" label>
        EXPECTED: Example:
        EXPECTED: **Shangong Golden Lions** *(selection name)*
        EXPECTED: Money Line *(market name)*
        EXPECTED: Shandong Golden Lions v Zhejiang Guangsha Lions  **10-15** LIVE
        EXPECTED: 10 - *home team score*
        EXPECTED: 15 - *away team score*
        EXPECTED: **FOR** **RELEASE** **98**
        EXPECTED: <Event name> <"LIVE" label> <Team 1 score> <Team 2 score>
        EXPECTED: Example:
        EXPECTED: **Shangong Golden Lions** *(selection name)*
        EXPECTED: Money Line *(market name)*
        EXPECTED: Shandong Golden Lions v Zhejiang Guangsha Lions LIVE **10-15**
        EXPECTED: 10 - *home team score*
        EXPECTED: 15 - *away team score*
        """
        pass

    def test_004_verify_score_correctness_for_each_team(self):
        """
        DESCRIPTION: Verify score correctness for each team
        EXPECTED: Score corresponds to the **'value'** attribute from WS
        """
        pass

    def test_005_verify_score_ordering_for_events(self):
        """
        DESCRIPTION: Verify score ordering for events
        EXPECTED: * 'Score' for the home team is shown at the same row as team name near the Price/Odds button (roleCode="HOME"/"TEAM_1")
        EXPECTED: * 'Score' for the away team s shown at the same row as team name near the Price/Odds button  (roleCode="AWAY"/"TEAM_2")
        """
        pass

    def test_006_verify_score_displaying_and_correctness_for_basketball_us_event(self):
        """
        DESCRIPTION: Verify score displaying and correctness for **Basketball US** event
        EXPECTED: * Format is the same as described in step 3
        EXPECTED: * Team names are switched (away team first)
        EXPECTED: * Away Team score is shown first, Home team score is shown last
        """
        pass

    def test_007_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have 'Live Score' available
        EXPECTED: * 'LIVE' label is shown
        EXPECTED: * 'Live Scores' are NOT displayed
        """
        pass

    def test_008_verify_live_score_for_outright_events(self):
        """
        DESCRIPTION: Verify 'Live Score' for 'Outright' events
        EXPECTED: * 'LIVE' label is shown
        EXPECTED: * 'Live Scores' are NOT displayed
        """
        pass

    def test_009_for_multiples_repeat_steps_2_8(self):
        """
        DESCRIPTION: For multiples repeat steps 2-8
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_2_9_for_cash_out_tab_my_bets_tab_bet_history_tab(self):
        """
        DESCRIPTION: Repeat steps 2-9 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'My Bets' tab
        DESCRIPTION: * 'Bet History' tab
        EXPECTED: 
        """
        pass
