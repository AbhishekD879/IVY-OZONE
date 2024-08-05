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
class Test_C1489604_Verify_Handball_Live_Score_change_for_HOME_AWAY_Player(Common):
    """
    TR_ID: C1489604
    NAME: Verify Handball Live Score change for HOME/AWAY Player
    DESCRIPTION: This test case verifies Handball Live Score change for HOME/AWAY Player on 'Cash Out', 'Open Bets', 'Bet History' tabs
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

    def test_003_change_the_score_for_home_team(self):
        """
        DESCRIPTION: Change the score for HOME team
        EXPECTED: * Score immediately starts displaying new value for Home player
        EXPECTED: * Update is received in WS and corresponds to **event.scoreboard.ALL.value** where **role_code=HOME**
        """
        pass

    def test_004_change_the_score_for_away_team(self):
        """
        DESCRIPTION: Change the score for AWAY team
        EXPECTED: * Score immediately starts displaying new value for Away player
        EXPECTED: * Update is received in WS and corresponds to **event.scoreboard.ALL.value** where **role_code=AWAY**
        """
        pass

    def test_005_verify_score_change_for_home_player_before_application_is_opened(self):
        """
        DESCRIPTION: Verify Score change for HOME player before application is opened
        EXPECTED: If application was not started/opened and Score was changed for HOME player, after opening application and cash out page with verified bet - updated Score will be shown there
        """
        pass

    def test_006_verify_score_change_for_away_player_before_application_is_opened(self):
        """
        DESCRIPTION: Verify Score change for AWAY player before application is opened
        EXPECTED: Same as step 5
        """
        pass

    def test_007_for_multiples_repeat_steps_2_5(self):
        """
        DESCRIPTION: For Multiples repeat steps 2-5
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_6_for_cash_out_tab_open_bets_tab__settled_bets_tab(self):
        """
        DESCRIPTION: Repeat steps 2-6 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'Open Bets' tab
        DESCRIPTION: *  'Settled Bets' tab
        EXPECTED: 
        """
        pass
