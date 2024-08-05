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
class Test_C1489600_Verify_Volleyball_Beach_Volleyball_Scores_displaying_in_My_Bets_section_when_PointsInCurrentSet_and_Set_are_changed_for_Home_player(Common):
    """
    TR_ID: C1489600
    NAME: Verify Volleyball/Beach Volleyball Scores displaying in 'My Bets' section when PointsInCurrentSet and Set are changed for Home player
    DESCRIPTION: This test case verifies Volleyball/Beach Volleyball Scores displaying on 'Cash Out', 'Open Bets', 'Bet History' tabs when PointsInCurrentSet and Set are changed for Home player
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

    def test_003_change_pointsincurrentset_in_betgenius_tool_or_in_ob_ti_tool_within_event_name_for_home_player(self):
        """
        DESCRIPTION: Change PointsInCurrentSet in BetGenius tool or in OB TI tool within event name for HOME player
        EXPECTED: * PointsInCurrentSet immediately starts displaying new value for Home player
        EXPECTED: * PointsInCurrentSet corresponds to **event.scoreboard.CURRENT.value** received in WS where **role_code=HOME**
        """
        pass

    def test_004_change_set_score_in_betgenius_tool_or_ob_ti_tool_within_event_name_for_home_player(self):
        """
        DESCRIPTION: Change Set score in BetGenius tool or OB TI tool within event name for HOME player
        EXPECTED: * Set immediately starts displaying new value for Away player
        EXPECTED: * Set corresponds to **event.scoreboard.ALL.value** received in WS where **role_code=HOME**
        EXPECTED: * PointsInCurrentSet are updated automatically and corresponds to **event.scoreboard.CURRENT.value** received in WS where **role_code=HOME**
        """
        pass

    def test_005_verify_pointsincurrentset_and_set_change_before_application_is_opened(self):
        """
        DESCRIPTION: Verify PointsInCurrentSet and Set change before application is opened
        EXPECTED: If application was not started/opened and PointsInCurrentSet and Set were changed for HOME player, after opening application and cash out page with verified bet - updated PointsInCurrentSet will be shown there
        """
        pass

    def test_006_for_multiples_repeat_steps_2_5(self):
        """
        DESCRIPTION: For multiples repeat steps 2-5
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_2_6_for_beach_volleyball(self):
        """
        DESCRIPTION: Repeat steps 2-6 for Beach Volleyball
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_7_for_cash_out_tab_open_bets_tab_bet_history_tab(self):
        """
        DESCRIPTION: Repeat steps 2-7 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'Open Bets' tab
        DESCRIPTION: * 'Bet History' tab
        EXPECTED: 
        """
        pass
