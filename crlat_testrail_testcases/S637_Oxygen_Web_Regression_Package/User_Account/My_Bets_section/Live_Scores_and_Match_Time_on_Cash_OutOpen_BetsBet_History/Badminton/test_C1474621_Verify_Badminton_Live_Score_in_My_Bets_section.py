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
class Test_C1474621_Verify_Badminton_Live_Score_in_My_Bets_section(Common):
    """
    TR_ID: C1474621
    NAME: Verify Badminton Live Score in My Bets section
    DESCRIPTION: This test case verifies Badminton Live score on 'Cash Out', 'Open Bets' and 'Bet History' tabs
    PRECONDITIONS: 1. User should be logged in to see their cash out/open bets/bet history
    PRECONDITIONS: 2. User should have placed bets on a Badminton live event with scores available
    PRECONDITIONS: 3. In order to have Scores, Badminton event should be in-play
    PRECONDITIONS: 4. To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORTS::::LIVE_EVENT"
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **categoryCode** = "BADMINTON"
    PRECONDITIONS: *   **value** - to see a Game score for particular participant
    PRECONDITIONS: *   **role_code**='PLAYER_1' / **role_code**='PLAYER_2' - to determine HOME and AWAY teams
    PRECONDITIONS: 5. [How to generate Live Scores for Badminton][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+Updates+for+Volleyball%2C+Beach+Volleyball+and+Badminton
    """
    keep_browser_open = True

    def test_001_go_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Go to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: * Cash out page is opened
        EXPECTED: * User's cash out bets are shown
        """
        pass

    def test_002_verify_badminton_bet_with_game_scores_available(self):
        """
        DESCRIPTION: Verify Badminton bet with Game Scores available
        EXPECTED: * The bet is shown in the cash out section
        """
        pass

    def test_003_verify_game_score_and_point_score_displaying(self):
        """
        DESCRIPTION: Verify Game score and Point score displaying
        EXPECTED: * Game score is displayed next to the 'LIVE' label
        EXPECTED: * Game score and point score are displayed in the following format:
        EXPECTED: **FOR** **RELEASE** **99**
        EXPECTED: <Event name> <Player 1 game score> <Player 1 point score> <Player 2 point score> <Player 2 game score><"LIVE" label>
        EXPECTED: Example:
        EXPECTED: KS Warta Zawiercie *(selection name)*
        EXPECTED: Match betting *(market name)*
        EXPECTED: KS Warta Zawiercie v Espadon Szczecin  0 **12-11** 1 LIVE
        EXPECTED: 0 - *player 1 game score*
        EXPECTED: 1 - *player 2 game score*
        EXPECTED: 12 - *player 1 point score*
        EXPECTED: 11 - *player 2 point score*
        EXPECTED: **FOR** **RELEASE** **98**
        EXPECTED: <Event name> <"LIVE" label> <Player 1 game score> <Player 1 point score> <Player 2 point score> <Player 2 game score>
        EXPECTED: Example:
        EXPECTED: KS Warta Zawiercie *(selection name)*
        EXPECTED: Match betting *(market name)*
        EXPECTED: KS Warta Zawiercie v Espadon Szczecin LIVE 0 **12-11** 1
        EXPECTED: 0 - *player 1 game score*
        EXPECTED: 1 - *player 2 game score*
        EXPECTED: 12 - *player 1 point score*
        EXPECTED: 11 - *player 2 point score*
        """
        pass

    def test_004_verify_game_score_correctness_for_each_player(self):
        """
        DESCRIPTION: Verify Game Score correctness for each player
        EXPECTED: * Game Score for Home team corresponds to **events.comments.team.player_1.score** attribute from WS response
        EXPECTED: * Game Score for Away team corresponds to **events.comments.team.player_2.score** attribute from WS response
        """
        pass

    def test_005_verify_points_score_correctness_for_each_player(self):
        """
        DESCRIPTION: Verify Points Score correctness for each player
        EXPECTED: Points Score for each team corresponds to **events.comments.setScores.[i]**
        EXPECTED: where i - the highest value
        """
        pass

    def test_006_verify_a_bet_placed_on_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify a bet placed on event which doesn't have LIVE Score available
        EXPECTED: * Scores are not shown
        EXPECTED: * 'LIVE' label is shown
        """
        pass

    def test_007_verify_game_and_points_scores_for_bet_placed_on_an_outright_event(self):
        """
        DESCRIPTION: Verify Game and Points Scores for bet, placed on an Outright event
        EXPECTED: * Scores are not shown for Outright events
        EXPECTED: * 'LIVE' label is shown
        """
        pass

    def test_008_for_multiples_repeat_steps_2_7(self):
        """
        DESCRIPTION: For multiples repeat steps 2-7
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_2_8_for_cash_out_tab_my_bets_tab_bet_history_tab(self):
        """
        DESCRIPTION: Repeat steps 2-8 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'My Bets' tab
        DESCRIPTION: * 'Bet History' tab
        EXPECTED: 
        """
        pass
