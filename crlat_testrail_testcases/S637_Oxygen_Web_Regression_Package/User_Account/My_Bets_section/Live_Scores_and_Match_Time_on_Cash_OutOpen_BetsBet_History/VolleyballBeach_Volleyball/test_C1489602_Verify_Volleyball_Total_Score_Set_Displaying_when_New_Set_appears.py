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
class Test_C1489602_Verify_Volleyball_Total_Score_Set_Displaying_when_New_Set_appears(Common):
    """
    TR_ID: C1489602
    NAME: Verify Volleyball Total Score (Set) Displaying when New Set appears
    DESCRIPTION: This test case verifies updated sets displaying when new set appears.
    DESCRIPTION: This test case should be repeated for mobile, tablet and desktop.
    PRECONDITIONS: * User should be logged in to see their cash out/open bets/bet history
    PRECONDITIONS: * User should have placed bets on a Volleyball and Beach Volleyball live event with scores available
    PRECONDITIONS: * In order to have Scores, Badminton event should be in-play
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

    def test_003_change_the_set_in_betgenius_tool_or_ob_ti_within_event_name(self):
        """
        DESCRIPTION: Change the set in BetGenius tool or OB TI within event name
        EXPECTED: *   Total score (Sets) and PointsInCurrentSet immediately appears
        EXPECTED: * **PointsInCurrentSet** corresponds to value received in event name in WS
        EXPECTED: * **Set** corresponds to the value in brackets received in event name in WS
        """
        pass

    def test_004_verify_new_set_appearing_before_application_is_opened(self):
        """
        DESCRIPTION: Verify new Set appearing before application is opened
        EXPECTED: If application was not started/opened and new set appears, after opening application and cash out page with verified bet - PointsInCurrentSet of new set and updated set number will be shown there
        """
        pass

    def test_005_repeat_steps_2_4_for_beach_volleyball(self):
        """
        DESCRIPTION: Repeat steps 2-4 for Beach Volleyball
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_2_5_for_cash_out_tab_open_bets_tab_bet_history_tab(self):
        """
        DESCRIPTION: Repeat steps 2-5 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'Open Bets' tab
        DESCRIPTION: * 'Bet History' tab
        EXPECTED: 
        """
        pass
