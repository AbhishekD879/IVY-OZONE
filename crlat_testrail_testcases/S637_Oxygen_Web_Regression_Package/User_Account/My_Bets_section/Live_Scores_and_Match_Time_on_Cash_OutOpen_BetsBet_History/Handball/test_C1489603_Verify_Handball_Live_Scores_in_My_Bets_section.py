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
class Test_C1489603_Verify_Handball_Live_Scores_in_My_Bets_section(Common):
    """
    TR_ID: C1489603
    NAME: Verify Handball Live Scores in 'My Bets' section
    DESCRIPTION: This test case verifies Handball Live Scores on 'Cash Out', 'Open Bets', 'Bet History' tabs
    DESCRIPTION: This test case should be repeated on mobile, tablet and desktop
    PRECONDITIONS: * User should be logged in to see their cash out/open bets/bet history
    PRECONDITIONS: * User should have placed bets on a Handball live event with scores available
    PRECONDITIONS: * In order to have Scores, Handball event should be in-play
    PRECONDITIONS: 1) In order to have a Scores Handball event should be in-play
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORTS::::LIVE_EVENT"
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **categoryCode** = "HANDBALL"
    PRECONDITIONS: *   **score** - to see a score for particular participant
    PRECONDITIONS: 3) Live Scores are received in event name from BetGenius or can be created manually in Openbet TI in next format:
    PRECONDITIONS: "|Team A Name|" ScoreA-ScoreB "|Team B Name|" ( e.g. |Saint Raphael| 25-18 |Selestat|(BG) )
    """
    keep_browser_open = True

    def test_001_go_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Go to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: * Cash out page is opened
        EXPECTED: * User's cash out bets are shown
        """
        pass

    def test_002_verify_handball_bet_with_game_scores_available(self):
        """
        DESCRIPTION: Verify Handball bet with Game Scores available
        EXPECTED: * The bet is shown in the cash out section
        EXPECTED: * Scores are displayed
        """
        pass

    def test_003_verify_score_displaying(self):
        """
        DESCRIPTION: Verify score displaying
        EXPECTED: * The score is displayed next to the "LIVE" label in the following format:
        EXPECTED: **FOR** **Release** **99**
        EXPECTED: <Event name> <home team score> - <away team score> <"LIVE" label">
        EXPECTED: Example:
        EXPECTED: BM Benidorm *(selection name)*
        EXPECTED: Match Betting *(market name)*
        EXPECTED: BM Benidom v SD Teucro **2-1** LIVE
        EXPECTED: **FOR** **Release** **98**
        EXPECTED: <Event name> <"LIVE" label"> <home team score> - <away team score>
        EXPECTED: Example:
        EXPECTED: BM Benidorm *(selection name)*
        EXPECTED: Match Betting *(market name)*
        EXPECTED: BM Benidom v SD Teucro LIVE **2-1**
        """
        pass

    def test_004_verify_score_correctness_for_home_team(self):
        """
        DESCRIPTION: Verify score correctness for Home team
        EXPECTED: Score corresponds to the **events.[i].comments.teams.home.score'** attribute from the WS,
        EXPECTED: where [i] - number of event that contains particular class
        """
        pass

    def test_005_verify_score_correctness_for_away_team(self):
        """
        DESCRIPTION: Verify score correctness for Away team
        EXPECTED: Score corresponds to the **events.[i].comments.teams.home.score'** attribute from the WS,
        EXPECTED: where [i] - number of event that contains particular class
        """
        pass

    def test_006_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have LIVE Score available
        EXPECTED: * Scores are not shown
        EXPECTED: * Only 'LIVE' label is shown next to the event name
        """
        pass

    def test_007_verify_scores_for_outright_event(self):
        """
        DESCRIPTION: Verify Scores for Outright event
        EXPECTED: * Scores are not shown for Outright events
        EXPECTED: * Only 'LIVE' label is shown next to the event name
        """
        pass

    def test_008_for_multiples_repeat_steps_2_7(self):
        """
        DESCRIPTION: For Multiples repeat steps 2-7
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_2_8_for_open_bets_tab_settled_bets_tab(self):
        """
        DESCRIPTION: Repeat steps 2-8 for:
        DESCRIPTION: * 'Open Bets' tab
        DESCRIPTION: * 'Settled Bets' tab
        EXPECTED: 
        """
        pass
