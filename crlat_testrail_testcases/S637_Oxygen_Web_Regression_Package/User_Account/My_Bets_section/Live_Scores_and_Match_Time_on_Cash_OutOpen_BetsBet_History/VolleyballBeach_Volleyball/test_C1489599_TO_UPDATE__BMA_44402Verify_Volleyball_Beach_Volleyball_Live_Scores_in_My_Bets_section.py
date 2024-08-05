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
class Test_C1489599_TO_UPDATE__BMA_44402Verify_Volleyball_Beach_Volleyball_Live_Scores_in_My_Bets_section(Common):
    """
    TR_ID: C1489599
    NAME: [TO UPDATE - BMA-44402]Verify Volleyball/Beach Volleyball Live Scores in 'My Bets' section
    DESCRIPTION: TO UPDATE ACCORDING TO NEW DESIGN BMA-44402
    DESCRIPTION: This test case verifies Volleyball and Beach Volleyball live scores displaying on 'Cash Out', 'My Bets' and 'Bet History' tabs
    DESCRIPTION: This test case should be repeated for mobile, tablet and desktop
    PRECONDITIONS: * User should be logged in to see their cash out/open bets/bet history
    PRECONDITIONS: * User should have placed bets on a Volleyball and Beach Volleyball live event with scores available
    PRECONDITIONS: * In order to have Scores, Volleyball event should be in-play
    PRECONDITIONS: 1) Create Volleyball and Beach Volleyball live event in OB tool using format |Team A Name| (SetsA) PointsInCurrentSetA-PointsInCurrentSetB (SetsB) |Team B Name|
    PRECONDITIONS: (e.g. |Volero Zurich Women| (2) 12-5 (0) |CS Volei Alba Blaj Women|(BG)|)
    PRECONDITIONS: Update scores within event name or receive events from BetGenius.
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Open+Bet+Systems
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Bet+Genius
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: ["IN_PLAY_SPORTS::::LIVE_EVENT",…]
    PRECONDITIONS: Look at the attributes on Event level:
    PRECONDITIONS: **teams** - home or away
    PRECONDITIONS: **name** - team name
    PRECONDITIONS: **score** - Set - total score for team - (displayed on FE in grey color)
    PRECONDITIONS: **currentPoints** - PointsInCurrentSet - current score for team (displayed on FE in black color)
    """
    keep_browser_open = True

    def test_001_go_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Go to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: * Cash out page is opened
        EXPECTED: * User's cash out bets are shown
        """
        pass

    def test_002_verify_volleyball_bet_with_game_scores_available(self):
        """
        DESCRIPTION: Verify Volleyball bet with Game Scores available
        EXPECTED: * The bet is shown in the cash out section
        EXPECTED: * Scores are displayed
        """
        pass

    def test_003_verify_total_score_sets_and_pointsincurrentset_displaying_for_event(self):
        """
        DESCRIPTION: Verify Total score (Sets) and PointsInCurrentSet displaying for event
        EXPECTED: * Total score (Sets) in grey color and PointsInCurrentSet in black color for particular team are shown next to the "LIVE" label in the following format:
        EXPECTED: **FOR** **Release** **99**
        EXPECTED: <Event name> <Total score player 1> <point score player 1> <point score player 2> <total score player 2> <"LIVE" label>
        EXPECTED: Example:
        EXPECTED: Indykpol AZS Olsztyn *(selection name)*
        EXPECTED: Match Betting *(market name)*
        EXPECTED: Indykpol AZS Olsztyn v ONICO Warszawa 2 **16-14** 1 LIVE
        EXPECTED: 2 - *Total score player 1*
        EXPECTED: 1 - *Total score player 2*
        EXPECTED: 16 - *point score player 1*
        EXPECTED: 14 - *point score player 2*
        EXPECTED: **FOR** **Release** **98**
        EXPECTED: <Event name> <"LIVE" label> <Total score player 1> <point score player 1> <point score player 2> <total score player 2>
        EXPECTED: Example:
        EXPECTED: Indykpol AZS Olsztyn *(selection name)*
        EXPECTED: Match Betting *(market name)*
        EXPECTED: Indykpol AZS Olsztyn v ONICO Warszawa LIVE 2 **16-14** 1
        EXPECTED: 2 - *Total score player 1*
        EXPECTED: 1 - *Total score player 2*
        EXPECTED: 16 - *point score player 1*
        EXPECTED: 14 - *point score player 2*
        """
        pass

    def test_004_verify_total_score_sets_correctness_for_each_player(self):
        """
        DESCRIPTION: Verify Total score (Sets) correctness for each player
        EXPECTED: Set corresponds to the **score** attribute from WS
        """
        pass

    def test_005_verify_volleyball_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify Volleyball event which doesn't have LIVE Score available
        EXPECTED: * Total score (Sets) and PointsInCurrentSet are NOT displayed on the card
        EXPECTED: * "LIVE" label is shown
        """
        pass

    def test_006_verify_total_score_sets_and_pointsincurrentset_for_outright_events(self):
        """
        DESCRIPTION: Verify 'Total score (Sets) and PointsInCurrentSet for 'Outright' events
        EXPECTED: * Total score (Sets) and PointsInCurrentSet are NOT displayed on the card
        EXPECTED: * "LIVE" label is shown
        """
        pass

    def test_007_for_multiples_repeat_steps_2_6(self):
        """
        DESCRIPTION: For Multiples repeat steps 2-6
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_7_for_beach_volleyball(self):
        """
        DESCRIPTION: Repeat steps 2-7 for Beach Volleyball
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
